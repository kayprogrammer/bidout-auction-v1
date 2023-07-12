from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from apps.common.utils import TestUtil
from apps.general.models import Review, SiteDetail

settings.TESTING = True


class TestGeneral(TestCase):
    home_url = reverse("home")
    subscriber_url = reverse("subscribe")

    def setUp(self):
        verified_user = TestUtil.verified_user()
        listing = TestUtil.create_listing(verified_user=verified_user)
        self.listing = listing["listing"]
        self.reviews = Review.objects.create(
            user=verified_user, text="This is a nice new platform", show=True
        )

    def test_home(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["listings"], [self.listing])
        self.assertQuerysetEqual(response.context["reviews"], [self.reviews])
        self.assertTrue(isinstance(response.context["site"], SiteDetail))

    def test_subscribe(self):
        # Check response validity
        response = self.client.post(
            self.subscriber_url, {"email": "test_subscriber@example.com"}
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
