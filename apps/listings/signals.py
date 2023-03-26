from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from .models import Listing, Category
from .test_data.listings import test_listings, test_categories
from datetime import timedelta
import os
from pathlib import Path
from django.core.files.base import ContentFile
from cloudinary_storage.storage import MediaCloudinaryStorage
import random
from apps.general.signals import custom_signal3, custom_signal4

User = get_user_model()

PARENT_DIR = Path(__file__).resolve().parent
test_images_directory = os.path.join(PARENT_DIR, "test_data/images")

@receiver(custom_signal3)
def create_test_categories(sender, **kwargs):
    categories = Category.objects.all().values_list(
        "name", flat=True
    )
    new_categories = []
    count = 0
    for category in test_categories:
        if not category in categories:
            count += 1
            if count == 1:
                print("###############################")
                print("#-CREATING-INITIAL-CATEGORIES-#")
                print("###############################")
                print("  ---------------------------  ")


            new_category = Category(
                name=category
            )
            new_categories.append(new_category)

    Category.objects.bulk_create(new_categories)
    if len(new_categories) > 0:
        print("##############################")
        print("#-INITIAL-CATEGORIES-CREATED-#")
        print("##############################\n")
    custom_signal4.send(sender=sender)

@receiver(custom_signal4)
def create_initial_listings(sender, **kwargs):
    listings = Listing.objects.all()
    if not listings.exists():
        print("#############################")
        print("#-CREATING-INITIAL-LISTINGS-#")
        print("#############################")
        print("  -------------------------  ")

        auctioneer = User.objects.get(email="testauctioneer@email.com")
        categories = Category.objects.all()
        listings = []
        for idx, image_file in enumerate(os.listdir(test_images_directory)):
            if image_file.endswith(".png"):
                image_path = os.path.join(test_images_directory, image_file)
                with open(image_path, "rb") as f:
                    file_name = os.path.basename(image_file)
                    file_content = ContentFile(f.read())

                    file_storage = MediaCloudinaryStorage()
                    file_path = file_storage.save(f"listings/{file_name}", file_content)
                    listing = Listing(
                        auctioneer=auctioneer,
                        name=test_listings[idx]["name"],
                        desc="Korem ipsum dolor amet, consectetur adipiscing elit. Maece nas in pulvinar neque. Nulla finibus lobortis pulvinar. Donec a consectetur nulla.",
                        price=test_listings[idx]["price"],
                        category=random.choice(categories),
                        closing_date=timezone.now() + timedelta(days=7 + idx),
                        image=file_path,
                    )
                    listings.append(listing)

        Listing.objects.bulk_create(listings)
        print("############################")
        print("#-INITIAL-LISTINGS-CREATED-#")
        print("############################\n")
