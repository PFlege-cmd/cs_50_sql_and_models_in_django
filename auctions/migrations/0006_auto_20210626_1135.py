# Generated by Django 3.2.3 on 2021-06-26 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='url',
        ),
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.FilePathField(blank=True, null=True, path='C:\\Users\\pfleg\\OneDrive\\Desktop\\LifeLongLearning\\EdX\\cs50_WebProgramming\\SqlModelsMigrations\\commerce\\auctions\\images'),
        ),
    ]