# Generated by Django 4.1.4 on 2023-03-25 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0003_alter_sitedetail_address_alter_sitedetail_email_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitedetail",
            options={"verbose_name_plural": "Site details"},
        ),
        migrations.RemoveField(
            model_name="review",
            name="name",
        ),
    ]
