from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Listing
from .test_data.listings import test_listings
from datetime import timedelta
import os
from pathlib import Path
from django.core.files.base import ContentFile
from cloudinary_storage.storage import MediaCloudinaryStorage

User = get_user_model()

PARENT_DIR = Path(__file__).resolve().parent
test_images_directory = os.path.join(PARENT_DIR, "test_data/images")


@receiver(post_migrate)
def create_initial_listings(sender, **kwargs):
    listings = Listing.objects.all()
    if not listings.exists():
        print(
            """
            #############################
            #-CREATING-INITIAL-LISTINGS-#
            #############################
            """
        )
        dir_list = os.listdir(test_images_directory)
        file_storage = MediaCloudinaryStorage()
        auctioneer = User.objects.filter(email="testauctioneer@email.com")
        if not auctioneer.exists():
            avatar = None
            for img in dir_list:
                if str(img) == "tester.png":
                    avatar = img
            image_path = os.path.join(test_images_directory, avatar)
            with open(image_path, "rb") as f:
                file_name = os.path.basename(avatar)
                file_content = ContentFile(f.read())
                file_path = file_storage.save(
                    f"listings/avatar/{file_name}", file_content
                )
                auctioneer = User.objects.create_user(
                    first_name="John",
                    last_name="Doe",
                    email="testauctioneer@email.com",
                    password="testauctioneer",
                    avatar=file_path,
                )
        else:
            auctioneer = auctioneer.get()

        listings = []
        dir_list.remove("tester.png")
        for idx, image_file in enumerate(dir_list):
            if image_file.endswith(".png"):
                image_path = os.path.join(test_images_directory, image_file)
                with open(image_path, "rb") as f:
                    file_name = os.path.basename(image_file)
                    file_content = ContentFile(f.read())
                    file_path = file_storage.save(f"listings/{file_name}", file_content)
                    listing = Listing(
                        auctioneer=auctioneer,
                        name=test_listings[idx]["name"],
                        desc="Korem ipsum dolor amet, consectetur adipiscing elit. Maece nas in pulvinar neque. Nulla finibus lobortis pulvinar. Donec a consectetur nulla.",
                        price=test_listings[idx]["price"],
                        closing_date=timezone.now() + timedelta(days=7 + idx),
                        image=file_path,
                    )
                    listings.append(listing)

        Listing.objects.bulk_create(listings)
        print(
            """
            ############################
            #-INITIAL-LISTINGS-CREATED-#
            ############################
            """
        )
