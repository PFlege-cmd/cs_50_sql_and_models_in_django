# Generated by Django 3.2.3 on 2021-07-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='auction_open',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]