import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from hr_system import settings
from hr_system.constants import YES_OR_NO_TYPES
from support_data.models import Country, Organization
from .constants import MONTHS, PAYROLL_YEARS


class PayrollCenter(models.Model):
    """docstring for PayrollCenter"""
    name = models.CharField(max_length=150)
    date_create = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.CharField(max_length=150, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET(None), null=True)

    def get_absolute_url(self):
        return reverse('payroll:payroll-center-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Account(models.Model):
    account_code = models.IntegerField()
    account_name = models.CharField(max_length=150)


class PayrollPeriod(models.Model):
    KV_MONTH = {
        'JANUARY': 1,
        'FEBRUARY': 2,
        'MARCH': 3,
        'APRIL': 4,
        'MAY': 5,
        'JUNE': 6,
        'JULY': 7,
        'AUGUST': 8,
        'SEPTEMBER': 9,
        'OCTOBER': 10,
        'NOVEMBER': 11,
        'DECEMBER': 12,
    }

    """docstring for PayrollPeriod"""
    _month = datetime.datetime.now().month
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.CASCADE)
    month = models.CharField(max_length=15, choices=MONTHS, default=MONTHS[_month - 1][1])
    year = models.IntegerField(choices=PAYROLL_YEARS, default=datetime.datetime.now().year)
    payroll_key = models.CharField(max_length=150, blank=True, null=False, default=None, unique=True)
    status = models.CharField(max_length=6, default='OPEN')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def to_dict(self):
        return {
            'id': self.pk, 'payroll_center': str(self.payroll_center),
            'month': self.month, 'year': self.year, 'payroll_key': self.payroll_key,
            'status': self.status
        }

    def get_absolute_url(self):
        return reverse('payroll:payroll-period-detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.payroll_key is None:
            payroll_key = f'Y{self.year}M{self.KV_MONTH[self.month]}C{self.payroll_center_id}'
            if PayrollPeriod.objects.filter(payroll_key=payroll_key):
                raise ValidationError(f'Pay roll period for this month already created')
            else:
                self.payroll_key = payroll_key

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

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
    description = models.CharField(max_length=150, null=True, blank=True)
    ed_category = models.ForeignKey(EarningDeductionCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    recurrent = models.CharField(max_length=3, choices=YES_OR_NO_TYPES)
    taxable = models.CharField(max_length=3, choices=YES_OR_NO_TYPES)
    account_code = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    export = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, default=YES_OR_NO_TYPES[1][0], null=True, blank=True)

    def get_absolute_url(self):
        return reverse('payroll:ed-type-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.ed_type


class Bank(models.Model):
    """docstring for Bank"""
    bank = models.CharField(max_length=150)
    sort_code = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('payroll:bank-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.bank


class Currency(models.Model):
    """docstring for Currency"""
    currency = models.CharField(max_length=150)
    description = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('payroll:currency-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.currency


class LSTRates(models.Model):
    lower_boundary = models.DecimalField(max_digits=12, decimal_places=2)
    upper_boundary = models.DecimalField(max_digits=12, decimal_places=2)
    fixed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)


class PAYERates(models.Model):
    lower_boundary = models.DecimalField(max_digits=12, decimal_places=2)
    upper_boundary = models.DecimalField(max_digits=12, decimal_places=2)
    fixed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=2)


class PayrollCenterEds(models.Model):
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.CASCADE)
    ed_type = models.ForeignKey(EarningDeductionType, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('payroll:payroll-center-eds-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.payroll_center.name}-{self.ed_type.ed_type}'
