from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django import forms
from PIL import Image
import os
images_folder = "/Users/pfleg/OneDrive/Desktop/LifeLongLearning/EdX/cs50_WebProgramming/SqlModelsMigrations/commerce/auctions/images/{0}"



def images_path(instance, filename):
    return images_folder.format(filename);


images_path = "C:\\Users\\pfleg\\OneDrive\\Desktop\\LifeLongLearning\\EdX\\cs50_WebProgramming\\SqlModelsMigrations\\commerce\\auctions\\images"

class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = (
        ('EL', 'electricity'),
        ('TOY', 'toy'),
        ('BK', 'book'),
        ('CL', 'clothing'),
    )
    
    watch_list = models.ManyToManyField(User, blank = True, related_name="watch_list")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    start_bid = models.IntegerField()
    category = models.CharField(max_length = 3, choices = CATEGORY)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_by")
    image = models.ImageField(upload_to = 'images', blank=True, null=True)
    auction_open = models.BooleanField()
    
    
    def __str__(self):
        return f"title:{self.title}, {self.description}, starting bid: {self.start_bid}, category: {self.category}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)
        
class ListingForm(forms.ModelForm):
    class Meta: 
        model = Listing
        fields = ['title','description','start_bid','category','image']
        
        
class Bids(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    auction_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"amount:{self.amount}, bid by: {self.created_by}, for item: {self.auction_item}"
    
class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']
    
class Comments(models.Model):
    comment = models.CharField(max_length=400)
    auction_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "posted_by")
    
    def __str__(self):
        return f"{self.comment}, for item: {self.auction_item}, posted by:  {self.posted_by}"
   
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']