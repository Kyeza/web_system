from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import (PayrollCenter, Bank, Currency, PayrollPeriod, LSTRates, PAYERates,
                            EarningDeductionCategory, EarningDeductionType)
from support_data.models import Nationality, DutyStation, Department, JobTitle, ContractType, \
    Relationship, Country, Grade
from .constants import MARITAL_STATUS, GENDER, EMP_STATUS
from .utils import get_image_filename


class User(AbstractUser):
    pass


class CostCentre(models.Model):
    cost_centre = models.CharField(max_length=15)
    description = models.CharField(max_length=100, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('users:cost-centre-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.cost_centre


class Employee(models.Model):
    """docstring for Employee"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    user_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True)
    mobile_number = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    sex = models.CharField(max_length=6, choices=GENDER)
    id_number = models.CharField('ID Number', max_length=30)
    passport_number = models.CharField(max_length=16, blank=True, null=True)
    residential_address = models.CharField('Residential address', max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    gross_salary = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    tin_number = models.IntegerField('TIN NUMBER', null=True, blank=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.DO_NOTHING)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=True)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.DO_NOTHING, null=True, blank=True)
    duty_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.DO_NOTHING, null=True, blank=True)
    contract_type = models.ForeignKey(ContractType, on_delete=models.DO_NOTHING, null=True, blank=True)
    appointment_date = models.DateField(default=timezone.now, null=True, blank=True)
    social_security = models.CharField('Pays Social Security', max_length=3, choices=YES_OR_NO_TYPES, null=True,
                                       blank=True)
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.DO_NOTHING, null=True)
    bank_1 = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name='first_bank', null=True, blank=True)
    bank_2 = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name='second_bank', null=True, blank=True)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    first_account_number = models.IntegerField('Account Number 1', null=True, blank=True)
    second_account_number = models.IntegerField('Account Number 2', null=True, blank=True)
    first_bank_percentage = models.IntegerField('Percentage', null=True, blank=True)
    second_bank_percentage = models.IntegerField('Percentage', null=True, blank=True)
    social_security_number = models.CharField(max_length=30, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, blank=True)
    kin_full_name = models.CharField(max_length=250, null=True, blank=True)
    kin_phone_number = models.CharField(max_length=12, null=True, blank=True)
    kin_email = models.EmailField(null=True, blank=True)
    kin_relationship = models.ForeignKey(Relationship, on_delete=models.DO_NOTHING, null=True, blank=True)
    dr_ac_code = models.CharField(max_length=30, null=True, blank=True)
    cr_ac_code = models.CharField(max_length=30, null=True, blank=True)
    employment_status = models.CharField(max_length=17, choices=EMP_STATUS, default=EMP_STATUS[0][0], blank=True)

    def clean_payroll_center(self):
        if self.payroll_center is None:
            raise ValidationError("Please enter employee 'Payroll center'.")

    def clean_gross_salary(self):
        if self.gross_salary is None:
            raise ValidationError("Please enter employee 'Gross salary'.")

    # TODO: add phone number validator
    def clean_phone_number(self):
        pass

    def clean(self):
        self.clean_payroll_center()
        self.clean_gross_salary()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        if self.appointment_date is None:
            self.appointment_date = timezone.now()
            super().save()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.user.get_full_name()}'


class PayrollProcessors(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    earning_and_deductions_type = models.ForeignKey(EarningDeductionType, on_delete=models.PROTECT, blank=True)
    earning_and_deductions_category = models.ForeignKey(EarningDeductionCategory, on_delete=models.PROTECT, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.SET_NULL, null=True, blank=True)
    payroll_key = models.CharField(max_length=150, blank=True, null=False,
                                   default=None, unique=True, primary_key=True, editable=False)

    def to_dict(self):
        data = {
            'payroll_key': self.payroll_key,
            'employee': self.employee,
            'earning_and_deductions_type': self.earning_and_deductions_type,
            'earning_and_deductions_category': self.earning_and_deductions_category,
            'amount': self.amount
        }
        return data

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.payroll_key is None:
            self.payroll_key = f'P{self.payroll_period_id}S{self.employee_id}K{self.earning_and_deductions_type_id}'

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.payroll_key}-{self.payroll_period.payroll_center}-{self.earning_and_deductions_type}'


class TerminatedEmployees(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    notice_date = models.DateField(default=timezone.now, null=True)
    exit_date = models.DateField(default=timezone.now, null=True)
    days_given = models.IntegerField(null=True)
    employable = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    reason = models.TextField()

    def __str__(self):
        return self.employee


class Project(models.Model):
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.CASCADE)
    project_code = models.CharField(max_length=20, primary_key=True)
    project_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:project-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.project_code


class SOF(models.Model):
    project_code = models.OneToOneField(Project, on_delete=models.CASCADE)
    sof_code = models.CharField(max_length=20)
    sof_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:sof-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.sof_code


class DEA(models.Model):
    sof_code = models.OneToOneField(SOF, on_delete=models.CASCADE)
    dea_code = models.CharField(max_length=20)
    dea_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:dea-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.dea_code


class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cost_center = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, null=True, blank=True)
    project_code = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    sof_code = models.ForeignKey(SOF, on_delete=models.SET_NULL, null=True, blank=True)
    dea_code = models.ForeignKey(DEA, on_delete=models.SET_NULL, null=True, blank=True)
    contribution_percentage = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.employee} project'
