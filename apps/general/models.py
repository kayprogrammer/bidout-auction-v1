from django.db import models

from apps.common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model

User = get_user_model()

class SiteDetail(TimeStampedUUIDModel):
    name = models.CharField(max_length=300, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=300, null=True)
    fb = models.CharField(max_length=300, null=True)
    tw = models.CharField(max_length=300, null=True)
    wh = models.CharField(max_length=300, null=True)
    ig = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

class Suscriber(TimeStampedUUIDModel):
    email = models.EmailField(null=True) 
    exported = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Reviews(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=300, null=True)
    show = models.BooleanField(default=False)
    text = models.TextField()
    
    def __str__(self):
        if self.user:
            return self.user
        return self.name