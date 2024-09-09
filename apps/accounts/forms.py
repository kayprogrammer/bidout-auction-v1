from typing import Any, Dict
from django import forms
from django.template.loader import render_to_string
from django.contrib.auth.forms import (
    PasswordResetForm,
    UserCreationForm,
    SetPasswordForm,
    UserChangeForm,
)
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from .models import Timezone
from .senders import Util, MessageThread

User = get_user_model()

# -----ADMIN USER CREATION AND AUTHENTICATION------------#
class CustomAdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "first_name", "last_name"]
        error_class = "error"


class CustomAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        error_class = "error"


# -----GENERAL USER CREATION AND AUTHENTICATION-------------#
class CustomErrorMessages:
    email = {
        "unique": "Email address already registered",
        "required": "This field is required",
        "invalid": "Enter a valid email address",
    }
    phone = {
        "unique": "Phone number already registered",
        "required": "This field is required",
    }
    tz = {
        "does_not_exist": "Invalid timezone",
    }


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=25,
        label="First name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=25,
        label="Last name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Your email address",
        error_messages=CustomErrorMessages.email,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    tz = forms.ModelChoiceField(
        label="Timezone",
        error_messages=CustomErrorMessages.tz,
        queryset=Timezone.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    terms_agreement = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"id": "termsApply"})
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "tz",
            "password1",
            "password2",
            "terms_agreement",
        ]


# ----------------------------------------------------------#


class CustomPasswordResetForm(PasswordResetForm):
    # Taken from django.contrib.auth.forms
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        user = User.objects.filter(email=to_email)
        if user.exists():
            context["name"] = f"{user[0].first_name} {user[0].last_name}"
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            context["name"]
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")
        email_message.send()
        # MessageThread(email_message).start()


class CustomSetPasswordForm(SetPasswordForm):
    # Taken from django.contrib.auth.forms
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )
