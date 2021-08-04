from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class User(AbstractUser):
    """Default django class User"""
    pass


class Ticket(models.Model):
    """Ticket class"""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="media/")
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """UserFollows"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user',)


class Review(models.Model):
    """Review class"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField(max_length=1024, validators=[ MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
