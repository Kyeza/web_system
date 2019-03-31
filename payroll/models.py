import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from hr_system.constants import YES_OR_NO_TYPES
from support_data.models import Country, Organization
from .constants import MONTHS, PAYROLL_YEARS, OPEN_OR_CLOSED


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


class PayrollPeriod(models.Model):
    """docstring for PayrollPeriod"""
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTHS, default=datetime.datetime.now().month)
    year = models.IntegerField(choices=PAYROLL_YEARS, default=datetime.datetime.now().year)
    payroll_key = models.CharField(max_length=150, blank=True, null=False, default=None)
    status = models.CharField(max_length=6, choices=OPEN_OR_CLOSED, default=OPEN_OR_CLOSED[1][0])

    def get_absolute_url(self):
        return reverse('payroll:payroll-period-detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.status == 'OPEN':
            open_periods = []
            center_payroll_periods = self.payroll_center.payrollperiod_set.all()

            if center_payroll_periods:
                for period in center_payroll_periods:
                    if period.status == 'OPEN':
                        open_periods.append(period)
                if len(open_periods) >= 1:
                    raise ValidationError(f'Can not set "Status: {self.status}", \nonly one  '
                                          f'Payroll period can be open at a time')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        if self.payroll_key is None:
            self.payroll_key = f'Y{self.year}M{self.month}C{self.payroll_center_id}'

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
