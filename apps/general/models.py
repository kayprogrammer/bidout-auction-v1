from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SiteDetail(TimeStampedUUIDModel):
    name = models.CharField(default="Kay's Auction House", max_length=300)
    email = models.EmailField(default="kayprogrammer1@gmail.com")
    phone = models.CharField(default="+2348133831036", max_length=300)
    address = models.CharField(default="234, Lagos, Nigeria", max_length=300)
    fb = models.CharField(
        default="https://facebook.com", max_length=300, verbose_name=(_("Facebook"))
    )
    tw = models.CharField(
        default="https://twitter.com", max_length=300, verbose_name=(_("Twitter"))
    )
    wh = models.CharField(
        default="https://wa.me/2348133831036",
        max_length=300,
        verbose_name=(_("Whatsapp")),
    )
    ig = models.CharField(
        default="https://instagram.com", max_length=300, verbose_name=(_("Instagram"))
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and SiteDetail.objects.exists():
            raise ValidationError("There can be only one Site Detail instance")

        return super(SiteDetail, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Site details"


class Subscriber(TimeStampedUUIDModel):
    email = models.EmailField(null=True)
    exported = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Review(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    show = models.BooleanField(default=False)
    text = models.TextField(max_length=100)

    def __str__(self):
        return self.user.full_name
