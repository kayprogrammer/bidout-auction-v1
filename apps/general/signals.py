from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import SiteDetail


@receiver(post_migrate)
def create_my_model(sender, **kwargs):
    site_detail = SiteDetail.objects.all()
    if not site_detail.exists():
        site_detail = SiteDetail.objects.create()
        site_detail.save()
