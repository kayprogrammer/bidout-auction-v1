from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from autoslug import AutoSlugField

from apps.common.models import TimeStampedUUIDModel


User = get_user_model()


class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-listings", kwargs={"category_slug": self.slug})

    def clean(self):
        if self.name == "Other":
            raise ValidationError("Name must not be 'Other'")

    class Meta:
        verbose_name_plural = "Categories"


class Listing(TimeStampedUUIDModel):
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    desc = models.TextField()
    category = models.ForeignKey(
        Category, related_name="listings", on_delete=models.SET_NULL, null=True
    )
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    closing_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="listings/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("listing-detail", kwargs={"listing_slug": self.slug})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = None
        return url

    @property
    def time_left(self):
        remaining_time = self.closing_date - timezone.now()
        remaining_seconds = remaining_time.total_seconds()

        if self.active == False or remaining_seconds < 0:
            return "Closed!!!"
        else:
            days, seconds = divmod(int(remaining_seconds), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            return f"-{days:02d}D :{hours:02d}H :{minutes:02d}M :{seconds:02d}S"

    @property
    def time_left_seconds(self):
        if not self.active:
            return 0
        remaining_time = self.closing_date - timezone.now()
        remaining_seconds = remaining_time.total_seconds()
        return remaining_seconds

    @property
    def get_highest_bid(self):
        highest_bid = 0.00
        related_bids = self.bids.all()
        if related_bids.exists():
            highest_bid = related_bids.aggregate(max_bid=Max("amount"))["max_bid"]
            highest_bid = related_bids.filter(amount=highest_bid).first().amount

        return highest_bid

    class Meta:
        ordering = ["-created_at"]


class Bid(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.listing.name} - ${self.amount}"

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["listing", "amount"],
                name="unique_listing_amount_bid",
            ),
            models.UniqueConstraint(
                fields=["user", "listing"],
                name="unique_user_listing_bid",
            ),
        ]


class WatchList(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=1000, null=True)

    def __str__(self):
        if self.user:
            return f"{self.listing.name} - {self.user.full_name}"
        return f"{self.listing.name} - {self.session_key}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "listing"],
                name="unique_user_listing_watchlist",
            ),
            models.UniqueConstraint(
                fields=["session_key", "listing"],
                name="unique_session_key_listing_watchlist",
            ),
        ]
