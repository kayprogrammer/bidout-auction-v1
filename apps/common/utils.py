from django.utils import timezone
from apps.accounts.models import User
from apps.listings.models import Category, Listing

from datetime import timedelta


class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
            "password": "testpassword",
        }
        user = User.objects.create(**user_dict)
        return user

    def verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
            "password": "testpassword",
        }
        user = User.objects.create(**user_dict)
        return user

    def another_verified_user():
        create_user_dict = {
            "first_name": "AnotherTest",
            "last_name": "UserVerified",
            "email": "anothertestverifieduser@example.com",
            "is_email_verified": True,
            "password": "anothertestverifieduser123",
        }
        user = User.objects.create(**create_user_dict)
        return user

    def create_listing(verified_user):
        # Create Category
        category = Category.objects.create(name="TestCategory")

        # Create Listing
        listing_dict = {
            "auctioneer": verified_user,
            "name": "New Listing",
            "desc": "New description",
            "category": category,
            "price": 1000.00,
            "closing_date": timezone.now() + timedelta(days=1),
        }
        listing = Listing.objects.create(**listing_dict)
        return {"user": verified_user, "listing": listing, "category": category}
