from django.db import models
from django.contrib.auth.models import AbstractUser
from config.model_utils.models import TimeStampedModel 
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, unique=True)
    favorite_products = models.ManyToManyField("products.Product", related_name="favorited_by", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']


class EmailVerification(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)