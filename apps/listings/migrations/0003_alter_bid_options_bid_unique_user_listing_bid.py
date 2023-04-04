# Generated by Django 4.1.4 on 2023-03-29 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0002_alter_bid_listing_bid_unique_listing_amount_bid"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bid",
            options={"ordering": ["-updated_at"]},
        ),
        migrations.AddConstraint(
            model_name="bid",
            constraint=models.UniqueConstraint(
                fields=("user", "listing"), name="unique_user_listing_bid"
            ),
        ),
    ]