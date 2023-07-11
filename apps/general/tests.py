from django.test import TestCase


class TestGeneral(TestCase):
    home_url = "/general/site-detail/"
    subscriber_url = "/general/subscribe/"

    def test_retrieve_sitedetail(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_subscribe(self):
        # Check response validity
        response = self.client.post(
            self.subscriber_url, {"email": "test_subscriber@example.com"}
        )
        self.assertEqual(response.status_code, 201)
