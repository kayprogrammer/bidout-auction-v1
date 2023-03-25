from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Listing(TimeStampedUUIDModel):
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, null=True)
    desc = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    closing_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="listings/")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = None
        return url

    @property
    def time_left(self):
        remaining_time = self.my_datetime_field - datetime.now()
        remaining_seconds = remaining_time.total_seconds()
        if remaining_seconds < 0:
            return "Expired"
        else:
            days, seconds = divmod(int(remaining_seconds), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            return f"{days}D :{hours:02d}H :{minutes:02d}M :{seconds:02d}S"

    class Meta:
        ordering = ["-created_at"]


class Bid(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.listing} - ${self.amount}"


class WatchList(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=1000, null=True)

    def __str__(self):
        if self.user:
            return f"{self.listing} - {self.user}"
        return f"{self.listing} - {self.session_key}"
