from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

def image_path(instance, filename):
    timestamp = datetime.now()

    return f'SellAdImages/{str(timestamp)}-{filename}'


class SellAd(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    posted_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    asked_price = models.FloatField()
    quantity = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)


class AdImages(models.Model):
    add_id = models.ForeignKey(SellAd, on_delete=models.CASCADE, related_name='images')
    product_img = models.ImageField(upload_to=image_path)