from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import SiteDetail, Review

User = get_user_model()


@receiver(post_migrate)
def create_site_detail(sender, **kwargs):
    site_detail = SiteDetail.objects.all()
    if not site_detail.exists():
        print(
            """
            #########################
            #-CREATING-SITE-DETAILS-#
            #########################
            """
        )
        site_detail = SiteDetail.objects.create()
        site_detail.save()
        print(
            """
            ########################
            #-SITE-DETAILS-CREATED-#
            ########################
            """
        )


@receiver(post_migrate)
def create_initial_reviews(sender, **kwargs):
    reviews = Review.objects.all()
    if not reviews.exists():
        print(
            """
            ############################
            #-CREATING-INITIAL-REVIEWS-#
            ############################
            """
        )
        user = User.objects.filter(email="testreviewer@email.com")
        if not user.exists():
            user = User.objects.create_user(
                first_name="John",
                last_name="Doe",
                email="testreviewer@email.com",
                password="testreviewer",
            )
        else:
            user = user.get()

        reviews = [
            Review(
                user=user,
                show=True,
                text="Maecenas vitae porttitor neque, ac porttitor nunc. Duis venenatis lacinia libero. Nam nec augue ut nunc vulputate tincidunt at suscipit nunc.",
            )
            for index in range(3)
        ]
        Review.objects.bulk_create(reviews)
        print(
            """
            ###########################
            #-INITIAL-REVIEWS-CREATED-#
            ###########################
            """
        )
