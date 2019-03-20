import datetime

from django.db import models

from support_data.models import Country, Organization
from hr_system.constants import YES_OR_NO_TYPES
from .constants import MONTHS, PAYROLL_YEARS


class PayrollCenter(models.Model):
    """docstring for PayrollCenter"""
    name = models.CharField(max_length=150)
    date_create = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    organization = models.OneToOneField(Organization, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class PayrollPeriod(models.Model):
    """docstring for PayrollPeriod"""
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTHS, default=datetime.datetime.now().month)
    year = models.IntegerField(choices=PAYROLL_YEARS, default=datetime.datetime.now().year)
    payroll_key = models.CharField(max_length=150, blank=True, null=False, default='Auto generated')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.payroll_key = f'Y{self.year}M{self.month}C{self.payroll_center.pk}'
        super().save(['payroll_key'])

    def __str__(self):
        return f'{self.payroll_center.name}-{self.payroll_key}'


class EarningDeductionCategory(models.Model):
    """docstring for EarningDeductionCategory"""
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class EarningDeductionType(models.Model):
    """docstring for EarningDeductionTypes"""
    ed_type = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    ed_category = models.ForeignKey(EarningDeductionCategory, on_delete=models.DO_NOTHING)
    recurrent = models.CharField(max_length=3, choices=YES_OR_NO_TYPES)
    taxable = models.CharField(max_length=3, choices=YES_OR_NO_TYPES)

    def __str__(self):
        return self.ed_type


class Bank(models.Model):
    """docstring for Bank"""
    bank = models.CharField(max_length=150)
    sort_code = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.bank


class Currency(models.Model):
    """docstring for Currency"""
    currency = models.CharField(max_length=150)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.currency
