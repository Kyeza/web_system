from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import PayrollCenter, Bank, Currency, PayrollPeriod, EarningDeductionCategory, EarningDeductionType
from support_data.models import Nationality, DutyStation, Department, JobTitle, ContractType, Relationship, Country, \
    Grade
from .constants import MARITAL_STATUS, GENDER, EMP_STATUS
from .utils import get_image_filename


class User(AbstractUser):
    pass


class Employee(models.Model):
    """docstring for Employee"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    user_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True)
    mobile_number = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateTimeField(default=timezone.now)
    sex = models.CharField(max_length=6, choices=GENDER)
    id_number = models.IntegerField('ID Number')
    passport_number = models.CharField(max_length=16, blank=True, null=True)
    residential_address = models.CharField('Residential address', max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    gross_salary = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    tin_number = models.IntegerField('TIN NUMBER', null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.DO_NOTHING)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.DO_NOTHING, null=True)
    duty_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.DO_NOTHING, null=True)
    contract_type = models.ForeignKey(ContractType, on_delete=models.DO_NOTHING, null=True)
    appointment_date = models.DateTimeField(default=timezone.now, null=True)
    social_security = models.CharField('Pays Social Security', max_length=3, choices=YES_OR_NO_TYPES, null=True)
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.DO_NOTHING, null=True)
    bank_1 = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name='first_bank', null=True)
    bank_2 = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name='second_bank', null=True)
    cost_centre = models.CharField(max_length=150, null=True)
    first_account_number = models.IntegerField('Account Number 1', null=True)
    second_account_number = models.IntegerField('Account Number 2', null=True)
    first_bank_percentage = models.IntegerField('Percentage', null=True)
    second_bank_percentage = models.IntegerField('Percentage', null=True)
    social_security_number = models.CharField(max_length=30, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True)
    kin_full_name = models.CharField(max_length=250, null=True)
    kin_phone_number = models.CharField(max_length=12, null=True)
    kin_email = models.EmailField(null=True)
    kin_relationship = models.ForeignKey(Relationship, on_delete=models.DO_NOTHING, null=True)
    employment_status = models.CharField(max_length=17, choices=EMP_STATUS, default=EMP_STATUS[0][0])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.appointment_date is None:
            self.appointment_date = timezone.now()
            super().save()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.user.username.capitalize()} Employee'


class PayrollProcessors(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    earning_and_deductions_type = models.ForeignKey(EarningDeductionType, on_delete=models.PROTECT)
    earning_and_deductions_category = models.ForeignKey(EarningDeductionCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.SET_NULL, null=True)
    payroll_key = models.CharField(max_length=150, blank=True, null=False, default=None, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.payroll_key is None:
            self.payroll_key = f'P{self.payroll_period_id}S{self.employee_id}K{self.earning_and_deductions_type_id}'

        super().save(force_insert, force_update, using, update_fields)
