from django.db import models
from django.contrib.auth.models import AbstractUser
from config.model_utils.models import TimeStampedModel 

class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, unique=True)
    favorite_products = models.ManyToManyField("products.Product", related_name="favorited_by", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']


