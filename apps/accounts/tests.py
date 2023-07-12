from django.test import TestCase
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.messages import get_messages
from django.http.cookie import SimpleCookie

from apps.accounts.forms import CustomUserCreationForm
from apps.accounts.models import Timezone
from apps.accounts.senders import email_verification_generate_token

from apps.common.utils import TestUtil
from unittest import mock
import uuid

settings.TESTING = True


class TestAccounts(TestCase):
    register_url = "/accounts/register/"

    verify_email_url = "/accounts/verify-email/"
    resend_activation_email_url = "/accounts/resend-activation-email/"

    reset_password_url = "/accounts/reset-password/"
    reset_password_sent_url = "/accounts/reset-password-sent/"
    reset_password_confirm_url = "/accounts/reset/"
    reset_password_complete_url = "/accounts/reset-password-complete/"

    login_url = "/accounts/login/"
    logout_url = "/accounts/logout/"

    def setUp(self):
        self.timezone = Timezone.objects.create(name="Africa/Lagos")
        self.new_user = TestUtil.new_user()
        verified_user = TestUtil.verified_user()
        self.verified_user = verified_user

    def test_signup_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertTrue(isinstance(response.context["form"], CustomUserCreationForm))

    def test_signup_post(self):
        email = "testregisteruser@example.com"
        password = "testblablaregistersdsssduserpassword12@"
        user_in = {
            "first_name": "Testregister",
            "last_name": "User",
            "email": email,
            "tz": self.timezone.pkid,
            "password1": password,
            "password2": password,
            "terms_agreement": True,
        }

        # Verify that a new user can be registered successfully
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.post(self.register_url, user_in)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get("form"))

        # Verify that a user with the same email cannot be registered again
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.post(self.register_url, user_in)
        self.assertIsNotNone(response.context.get("form").errors)

    def test_verify_email(self):
        new_user = self.new_user
        uid = urlsafe_base64_encode(force_bytes(new_user.id))
        token = email_verification_generate_token.make_token(new_user)

        # Verify that the email verification fails with an invalid link
        fake_uid = urlsafe_base64_encode(force_bytes(uuid.uuid4()))
        response = self.client.get(
            f"{self.verify_email_url}{fake_uid}/{token}/{new_user.id}/"
        )
        self.assertTemplateUsed(response, "accounts/email-activation-failed.html")

        # Verify that the email verification succeeds with a valid link
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.get(
            f"{self.verify_email_url}{uid}/{token}/{new_user.id}/"
        )
        self.assertRedirects(
            response,
            "/accounts/login/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_resend_activation_email(self):
        new_user = self.new_user

        # Verify that an error is raised when attempting to resend the activation email for a user that doesn't exist
        self.client.cookies = SimpleCookie({"activation_email": "invalid@email.com"})
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.get(
            self.resend_activation_email_url,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Not allowed!")

        # Verify that an unverified user can get a new email
        self.client.cookies = SimpleCookie({"activation_email": new_user.email})
        mock.patch("apps.accounts.senders.Util", new="")
        # Then, attempt to resend the activation email
        response = self.client.get(self.resend_activation_email_url)
        self.assertTemplateUsed(response, "accounts/email-activation-request.html")

        # Verify that a verified user cannot get a new email
        new_user.is_email_verified = True
        new_user.save()
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.get(
            self.resend_activation_email_url,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Email address already verified!")

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_post(self):
        new_user = self.new_user

        # Test for invalid credentials
        response = self.client.post(
            self.login_url,
            {"email": "invalid@email.com", "password": "invalidpassword"},
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Invalid credentials!")
        self.assertRedirects(
            response,
            "/accounts/login/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

        # Test for unverified credentials (email)
        mock.patch("apps.accounts.senders.Util", new="")
        response = self.client.post(
            self.login_url,
            {"email": new_user.email, "password": "testpassword"},
        )
        self.assertTemplateUsed(response, "accounts/email-activation-request.html")

        # Test for valid credentials and verified email address
        new_user.is_email_verified = True
        new_user.save()
        response = self.client.post(
            self.login_url,
            {"email": new_user.email, "password": "testpassword"},
        )
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    # def test_get_password_otp(self):
    #     verified_user = self.verified_user
    #     email = verified_user.email

    #     password = "testverifieduser123"
    #     user_dict = {"email": email, "password": password}

    #     mock.patch("apps.accounts.senders.Util", new="")
    #     # Then, attempt to get password reset token
    #     response = self.client.post(self.send_password_reset_otp_url, user_dict)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "success", "message": "Password otp sent"},
    #     )

    #     # Verify that an error is raised when attempting to get password reset token for a user that doesn't exist
    #     mock.patch("apps.accounts.senders.Util", new="")
    #     response = self.client.post(
    #         self.send_password_reset_otp_url,
    #         {"email": "invalid@example.com"},
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "failure", "message": "Incorrect Email"},
    #     )

    # def test_reset_password(self):
    #     verified_user = self.verified_user
    #     password_reset_data = {
    #         "email": verified_user.email,
    #         "password": "newtestverifieduserpassword123",
    #     }
    #     otp = "111111"

    #     # Verify that the password reset verification fails with an incorrect email
    #     response = self.client.post(
    #         self.set_new_password_url,
    #         {
    #             "email": "invalidemail@example.com",
    #             "otp": otp,
    #             "password": "newpassword",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "failure", "message": "Incorrect Email"},
    #     )

    #     # Verify that the password reset verification fails with an invalid otp
    #     password_reset_data["otp"] = otp
    #     response = self.client.post(
    #         self.set_new_password_url,
    #         password_reset_data,
    #     )
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "failure", "message": "Incorrect Otp"},
    #     )

    #     # Verify that password reset succeeds
    #     Otp.objects.create(user_id=verified_user.id, code=otp)
    #     password_reset_data["otp"] = otp
    #     mock.patch("apps.accounts.senders.Util", new="")
    #     response = self.client.post(
    #         self.set_new_password_url,
    #         password_reset_data,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "success", "message": "Password reset successful"},
    #     )

    # def test_logout(self):
    #     auth_token = TestUtil.auth_token(self.verified_user)

    #     # Ensures if authorized user logs out successfully
    #     bearer = {"HTTP_AUTHORIZATION": f"Bearer {auth_token}"}
    #     response = self.client.get(self.logout_url, **bearer)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "success", "message": "Logout successful"},
    #     )

    #     # Ensures if unauthorized user cannot log out
    #     self.bearer = {"HTTP_AUTHORIZATION": f"invalid_token"}
    #     response = self.client.get(self.logout_url, **self.bearer)
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(
    #         response.json(),
    #         {"status": "failure", "message": "Auth Token is Invalid or Expired!"},
    #     )
