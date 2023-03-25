# Generated by Django 4.1.4 on 2023-03-25 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="listing",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RenameField(
            model_name="listing",
            old_name="creator",
            new_name="auctioneer",
        ),
        migrations.AddField(
            model_name="listing",
            name="image",
            field=models.ImageField(default=None, upload_to="listings/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="listing",
            name="name",
            field=models.CharField(max_length=70, null=True),
        ),
    ]