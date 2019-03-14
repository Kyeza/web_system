from django.db import models
from django.contrib.auth.models import User

from .utils import get_image_filename


# Create your models here.
class Profile(models.Model):
    """docstring for Profile"""
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARITAL_STATUS = (
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('SEPARATED', 'Separated'),
        ('DIVORCED', 'Divorced'),
        ('WIDOW', 'Widow')
    )

    NATIONALITY = (
        ('DJIBOUTI', 'Djibouti'),
        ('ETHIOPIAN', 'Ethiopian'),
        ('KENYAN', 'Kenyan'),
        ('SOMALI', 'Somali'),
        ('TANZANIAN', 'Tanzanian'),
        ('YEMENI', 'Yemeni'),
        ('UGANDAN', 'Ugandan'),
        ('OTHER', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True)
    mobile_number = models.CharField(max_length=12, blank=True, unique=True)
    date_of_birth = models.DateTimeField()
    sex = models.CharField(max_length=1, choices=GENDER)
    id_number = models.IntegerField('ID Number')
    passport_number = models.CharField(max_length=16, blank=True, unique=True)
    nationality = models.CharField(max_length=36, choices=NATIONALITY)
    address = models.CharField('Residential address', max_length=30, blank=True)
    town = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

