from django.db import models
from django.urls import reverse
from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from django.utils import timezone
from autoslug import AutoSlugField

User = get_user_model()


class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-listings", kwargs={"category_slug": self.slug})

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
        if remaining_seconds < 0:
            return "Closed!!!"
        else:
            days, seconds = divmod(int(remaining_seconds), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            return f"-{days:02d}D :{hours:02d}H :{minutes:02d}M :{seconds:02d}S"

    @property
    def time_left_seconds(self):
        remaining_time = self.closing_date - timezone.now()
        remaining_seconds = remaining_time.total_seconds()
        return remaining_seconds

    class Meta:
        ordering = ["-created_at"]


class Bid(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.listing.name} - ${self.amount}"


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
