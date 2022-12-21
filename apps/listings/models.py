from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Listing(TimeStampedUUIDModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 300, null=True)
    desc = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True) 
    closing_date = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Bid(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.listing} - ${self.amount}"

class WatchList(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=1000, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        if self.user:
            return f"{self.listing} - {self.user}"
        return f"{self.listing} - {self.session_key}"
