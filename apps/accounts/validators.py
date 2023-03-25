from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if (
            not any(char.isdigit() for char in password)
            or not any(char.isalpha() for char in password)
            or not any(char in special_characters for char in password)
        ):
            raise ValidationError(
                _("Passwords must contain letters, numbers and special characters.")
            )
        if len(password) < 8:
            raise ValidationError(
                _("Password must contain at least 8 characters"),
                code="password_too_short",
            )

    def get_help_text(self):
        return _(
            "Passwords must contain letters, numbers and special characters. It must also contain at least 8 characters"
        )
