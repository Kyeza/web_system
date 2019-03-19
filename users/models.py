from django.db import models
from django.contrib.auth.models import User, Group

from .utils import get_image_filename
from .users_constants import MARITAL_STATUS, GENDER


class Profile(models.Model):
    """docstring for Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_group = models.ForeignKey(Group, on_delete=models.SET(None))
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True)
    mobile_number = models.CharField(max_length=12, blank=True)
    date_of_birth = models.DateTimeField()
    sex = models.CharField(max_length=1, choices=GENDER)
    id_number = models.IntegerField('ID Number')
    passport_number = models.CharField(max_length=16, blank=True)
    nationality = models.CharField(max_length=36)
    address = models.CharField('Residential address', max_length=30, blank=True)
    town = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username.capitalize()} Profile'


class Country(models.Model):
    """docstring for Countries"""
    name = models.CharField(max_length=36)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    """docstring for Nationality"""
    country = models.OneToOneField(Country, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=36)

    def __str__(self):
        return self.name
