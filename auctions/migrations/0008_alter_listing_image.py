# Generated by Django 3.2.3 on 2021-06-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='null', upload_to='images'),
            preserve_default=False,
        ),
    ]