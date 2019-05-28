import datetime

from django.db import models
from django.urls import reverse

from hr_system.constants import YES_OR_NO_TYPES
from .constants import TAX_YEAR_CHOICES
from payroll.models import EarningDeductionType


class Country(models.Model):
    """docstring for Countries"""
    country_name = models.CharField(max_length=36)
    country_code = models.CharField(max_length=3)

    def get_absolute_url(self):
        return reverse('support_data:country-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.country_name


class Nationality(models.Model):
    """docstring for Nationality"""
    country = models.OneToOneField(Country, on_delete=models.CASCADE, primary_key=True)
    country_nationality = models.CharField(max_length=36)

    def get_absolute_url(self):
        return reverse('support_data:nationality-detail-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.country_nationality


class DutyStation(models.Model):
    """docstring for DutyStation"""
    duty_station = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    earnings_type = models.ForeignKey(EarningDeductionType, on_delete=models.SET_NULL, null=True, blank=True)
    earning_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('support_data:duty-station-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.duty_station


class Department(models.Model):
    """docstring for Department"""
    department = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('support_data:department-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.department


class JobTitle(models.Model):
    """docstring for JobTitle"""
    job_title = models.CharField(max_length=200)
    description = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('support_data:job-title-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.job_title


class ContractType(models.Model):
    """docstring for ContractType"""
    contract_type = models.CharField(max_length=150, null=True, blank=True)
    contract_expiry = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    leave_entitled = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    leave_days_entitled = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('support_data:contract-type-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.contract_type


class Relationship(models.Model):
    """docstring for Relationship"""
    relationship = models.CharField(max_length=150)

    def __str__(self):
        return self.relationship


class Organization(models.Model):
    """docstring for Organization"""
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('support_data:organization-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Grade(models.Model):
    """docstring for Grade"""
    grade = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.grade


class Tax(models.Model):
    """docstring for Taxes"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    lower_boundary = models.DecimalField(max_digits=7, decimal_places=2)
    upper_boundary = models.DecimalField(max_digits=7, decimal_places=2)
    fixed_amount = models.DecimalField(max_digits=7, decimal_places=2)
    year = models.IntegerField(choices=TAX_YEAR_CHOICES, default=datetime.datetime.now().year)

    def get_absolute_url(self):
        return reverse('support_data:tax-bracket-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.country
