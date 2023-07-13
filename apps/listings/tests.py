from django.test import TestCase
from django.conf import settings
from django.http import HttpResponseNotFound
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from apps.common.utils import TestUtil

from apps.listings.models import Bid, WatchList
from apps.listings.forms import CreateListingForm, UpdateProfileForm

from datetime import timedelta
from io import BytesIO
from PIL import Image
import json

settings.TESTING = True

bts = BytesIO()


class TestListings(TestCase):
    all_auctions_url = "/listings/"
    auctions_by_categories_url = "/categories/"
    watchlist_url = "/watch-list/"
    create_listing_url = "/create-listing/"
    dashboard_url = "/dashboard/"
    dashboard_profile_url = "/dashboard/?page=profile"
    dashboard_listings_url = "/dashboard/listings/"
    maxDiff = None

    def setUp(self):
        verified_user = TestUtil.verified_user()
        self.verified_user = verified_user
        self.listing = TestUtil.create_listing(verified_user)["listing"]
        self.another_verified_user = TestUtil.another_verified_user()

    def test_all_auctions_view(self):
        listing = self.listing
        # Verify that all listings are retrieved successfully
        response = self.client.get(self.all_auctions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/general/listings.html")
        self.assertQuerysetEqual(response.context["listings"], [listing])
        self.assertQuerysetEqual(response.context["categories"], [listing.category])

    def test_auction_detail_view(self):
        listing = self.listing
        # Verify that a particular listing retrieval fails with an invalid slug
        response = self.client.get(f"{self.all_auctions_url}invalid_slug/")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # Verify that a particular listing is retrieved successfully
        response = self.client.get(f"{self.all_auctions_url}{listing.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/general/listing-detail.html")
        self.assertEqual(response.context["listing"], listing)

    def test_auctions_by_category_view(self):
        listing = self.listing
        slug = listing.category.slug

        # Verify that listings by an invalid category slug fails
        response = self.client.get(
            f"{self.auctions_by_categories_url}invalid_category_slug/"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # Verify that all listings by a valid category slug are retrieved successfully
        response = self.client.get(f"{self.auctions_by_categories_url}{slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/general/listings.html")
        self.assertQuerysetEqual(response.context["listings"], [listing])
        self.assertEqual(response.context["category"], listing.category)

    def test_watchlist_view(self):
        listing = self.listing
        user = self.verified_user
        self.client.login(email=user.email, password="testpassword")

        # GET
        watchlist = WatchList.objects.create(user=user, listing=listing)
        response = self.client.get(self.watchlist_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/general/watchlist.html")
        self.assertQuerysetEqual(response.context["listings"], [watchlist])

        # POST
        # Verify that the request fails with an invalid slug
        response = self.client.post(
            self.watchlist_url,
            data=json.dumps({"listing_slug": "invalid_slug"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # Verify that the watchlist was created successfully
        response = self.client.post(
            self.watchlist_url,
            data=json.dumps({"listing_slug": listing.slug}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

        # DELETE
        response = self.client.delete(
            self.watchlist_url,
            data=json.dumps({"listing_slug": listing.slug}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "left": 0})

    def test_place_bid_view(self):
        listing = self.listing
        user = self.verified_user
        another_verified_user = self.another_verified_user
        self.client.login(email=user.email, password="testpassword")

        # Verify that the request fails with an invalid slug
        response = self.client.post(
            f"{self.all_auctions_url}invalid_category_slug/place-bid/",
            data={"amount": 10000},
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # Verify that the request fails with an invalid user
        response = self.client.post(
            f"{self.all_auctions_url}{listing.slug}/place-bid/",
            data={"amount": 10000},
        )
        self.assertEqual(
            response.json(),
            {"status": "error", "message": "You can't bid your product!"},
        )

        self.client.login(
            email=another_verified_user.email, password="anothertestverifieduser123"
        )
        # Verify that the request fails with a lesser bidding price
        response = self.client.post(
            f"{self.all_auctions_url}{listing.slug}/place-bid/",
            data={"amount": 100},
        )
        self.assertEqual(
            response.json(),
            {
                "status": "error",
                "message": "Bid amount cannot be less than the bidding price!",
            },
        )

        # Verify that the bid was created successfully
        response = self.client.post(
            f"{self.all_auctions_url}{listing.slug}/place-bid/",
            data={"amount": 10000},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"status": "success", "amount": "10,000.00", "page": None}
        )

        # You can also test for other error responses.....

    def test_dashboard_view(self):
        user = self.verified_user
        listing = self.listing
        self.client.force_login(user)

        # GET
        # For listings
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/main.html")
        self.assertQuerysetEqual(response.context["listings"], [listing])

        # For Profile
        response = self.client.get(self.dashboard_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/main.html")
        self.assertEqual(response.context["profile"], True)
        self.assertIsInstance(response.context["form"], UpdateProfileForm)

        # POST
        img = Image.new("RGB", (100, 100))
        img.save(bts, "jpeg")
        user_dict = {
            "first_name": "TestUpdated",
            "last_name": "VerifiedUpdated",
            "avatar": SimpleUploadedFile("test.jpg", bts.getvalue()),
        }
        response = self.client.post(
            self.dashboard_profile_url,
            data=user_dict,
        )
        self.assertRedirects(
            response,
            self.dashboard_profile_url,
            status_code=302,
            target_status_code=200,
        )

    def test_create_listing_view(self):
        user = self.verified_user
        listing = self.listing
        self.client.login(email=user.email, password="testpassword")

        # GET
        response = self.client.get(
            self.create_listing_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/create-listing.html")
        self.assertQuerysetEqual(response.context["categories"], [listing.category])
        self.assertIsInstance(response.context["form"], CreateListingForm)

        # POST
        img = Image.new("RGB", (100, 100))
        img.save(bts, "jpeg")
        listing_dict = {
            "name": "Test Listing",
            "desc": "Test description",
            "category": listing.category.slug,
            "price": 1000.00,
            "closing_date": timezone.now() + timedelta(days=7),
            "image": SimpleUploadedFile("test.jpg", bts.getvalue()),
        }
        response = self.client.post(self.create_listing_url, data=listing_dict)
        self.assertRedirects(
            response,
            "/dashboard/listings/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    # You can test for error responses

    def test_update_listing_view(self):
        user = self.verified_user
        listing = self.listing
        self.client.login(email=user.email, password="testpassword")

        # GET
        # For invalid slug
        response = self.client.get(f"{self.dashboard_listings_url}invalid_slug/update/")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # For valid slug
        response = self.client.get(
            f"{self.dashboard_listings_url}{listing.slug}/update/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/create-listing.html")
        self.assertEqual(response.context["listing"], listing)
        self.assertIsInstance(response.context["form"], CreateListingForm)
        self.assertQuerysetEqual(response.context["categories"], [listing.category])

        # POST
        img = Image.new("RGB", (100, 100))
        img.save(bts, "jpeg")
        listing_dict = {
            "name": "Test Listing Update",
            "desc": "Test description Update",
            "category": listing.category.slug,
            "price": 2000.00,
            "closing_date": timezone.now() + timedelta(days=7),
            "image": SimpleUploadedFile("test.jpg", bts.getvalue()),
        }
        response = self.client.post(
            f"{self.dashboard_listings_url}{listing.slug}/update/", data=listing_dict
        )
        self.assertRedirects(
            response,
            "/dashboard/listings/test-listing-update/update/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_update_listing_status_view(self):
        listing = self.listing
        self.client.force_login(self.verified_user)

        # For invalid slug
        response = self.client.get(
            f"{self.all_auctions_url}invalid_slug/status/update/"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # For valid slug
        response = self.client.get(
            f"{self.all_auctions_url}{listing.slug}/status/update/"
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_auctioneer_listings_view(self):
        listing = self.listing
        self.client.force_login(self.verified_user)

        # Verify that all listings by an authenticated auctioneer are retrieved successfully
        response = self.client.get(self.dashboard_listings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/all-listings.html")
        self.assertQuerysetEqual(response.context["listings"], [listing])

    def test_auctioneer_listing_bids_view(self):
        listing = self.listing
        another_verified_user = self.another_verified_user
        self.client.force_login(self.verified_user)

        bid = Bid.objects.create(
            user=another_verified_user, listing=listing, amount=10000.00
        )

        # Verify that listings by an invalid listing slug fails
        response = self.client.get(f"{self.dashboard_listings_url}invalid_slug/bids/")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponseNotFound)

        # Verify that all bids by a valid listing slug are retrieved successfully
        response = self.client.get(f"{self.dashboard_listings_url}{listing.slug}/bids/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/dashboard/bids.html")
        self.assertEqual(response.context["listing"], listing)
        self.assertQuerysetEqual(response.context["bids"], [bid])
