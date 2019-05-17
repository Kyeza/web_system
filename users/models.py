import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
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
    class Meta:
        permissions = [
            ("approve_employee", "Can approve Employee"),
        ]


class CostCentre(models.Model):
    cost_centre = models.CharField(max_length=15)
    description = models.CharField(max_length=100, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('users:cost-centre-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.cost_centre


class District(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """docstring for Employee"""
    phone_number_regex = re.compile(r'^\+?1?\d{9,15}$')
    validation_msg = 'Enter a valid phone number .i.e: +0700000000 or +256700000000'
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, editable=False)
    user_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True,
                                     validators=[RegexValidator(inverse_match=True, regex=phone_number_regex,
                                                                message=validation_msg)])
    date_of_birth = models.DateField(default=timezone.now)
    sex = models.CharField(max_length=6, choices=GENDER)
    id_number = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=200, blank=True, null=True)
    home_address = models.CharField(max_length=200, blank=True, null=True)
    residential_address = models.CharField(max_length=200, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    tin_number = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    duty_station = models.ForeignKey(DutyStation, on_delete=models.SET_NULL, null=True, blank=True)
    duty_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    reports_to = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                   related_name='reports_to', null=True, blank=True)
    contract_type = models.ForeignKey(ContractType, on_delete=models.SET_NULL, null=True, blank=True)
    contract_expiry = models.DateField(null=True, blank=True)
    appointment_date = models.DateField(default=timezone.now, null=True, blank=True)
    social_security = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    payroll_center = models.ForeignKey(PayrollCenter, on_delete=models.SET_NULL, null=True)
    bank_1 = models.ForeignKey(Bank, on_delete=models.SET_NULL, related_name='first_bank', null=True, blank=True)
    bank_2 = models.ForeignKey(Bank, on_delete=models.SET_NULL, related_name='second_bank', null=True, blank=True)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, null=True, blank=True, )
    first_account_number = models.CharField(max_length=200, null=True, blank=True)
    second_account_number = models.CharField(max_length=200, null=True, blank=True)
    first_bank_percentage = models.IntegerField(null=True, blank=True, default=0)
    second_bank_percentage = models.IntegerField(null=True, blank=True, default=0)
    social_security_number = models.CharField(max_length=200, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    kin_full_name = models.CharField(max_length=250, null=True, blank=True)
    kin_phone_number = models.CharField(max_length=15, blank=True, null=True,
                                        validators=[RegexValidator(inverse_match=True, regex=phone_number_regex,
                                                                   message=validation_msg)])
    kin_email = models.EmailField(null=True, blank=True)
    kin_relationship = models.ForeignKey(Relationship, on_delete=models.SET_NULL, null=True, blank=True)
    dr_ac_code = models.CharField(max_length=50, null=True, blank=True)
    cr_ac_code = models.CharField(max_length=50, null=True, blank=True)
    employment_status = models.CharField(max_length=17, choices=EMP_STATUS, default=EMP_STATUS[0][0], blank=True)
    agresso_number = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def clean(self):
        user_with_id_no = Employee.objects.filter(id_number__exact=self.id_number).first() if self.id_number else None
        if user_with_id_no.pk != self.pk:
            raise ValidationError("ID number already exists.")

        user_with_passport_no = Employee.objects.filter(id_number__exact=self.passport_number).first() if self.passport_number else None
        if user_with_passport_no:
            if user_with_passport_no.pk != self.pk:
                raise ValidationError("Passport number already exists.")

        user_with_agresso_no = Employee.objects.filter(id_number__exact=self.agresso_number) if self.agresso_number else None
        if user_with_agresso_no:
            if user_with_agresso_no != self.pk:
                raise ValidationError("Agresso number already exists.")

        if self.payroll_center is None:
            raise ValidationError("Payroll Canter required.")

        if self.gross_salary is None:
            raise ValidationError("Basic salary required.")

        if self.first_bank_percentage > 0:
            if self.bank_1 is None:
                raise ValidationError("Bank 1 required.")
            if self.first_account_number is None:
                raise ValidationError("Account 1 required.")

        if self.second_bank_percentage > 0:
            if self.bank_2 is None:
                raise ValidationError("Bank 2 required.")
            if self.second_account_number is None:
                raise ValidationError("Account 2 required.")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return ' '.join([name.capitalize() for name in f'{self.user}'.split('.')])


class PayrollProcessors(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    earning_and_deductions_type = models.ForeignKey(EarningDeductionType, on_delete=models.PROTECT, blank=True)
    earning_and_deductions_category = models.ForeignKey(EarningDeductionCategory, on_delete=models.PROTECT, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.SET_NULL, null=True, blank=True)
    payroll_key = models.CharField(max_length=150, blank=True, null=False, unique=True, primary_key=True, editable=False)

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
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    notice_date = models.DateField(default=timezone.now, null=True, blank=True)
    exit_date = models.DateField(default=timezone.now, null=True, blank=True)
    days_given = models.PositiveIntegerField(null=True, blank=True)
    employable = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

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
    project_key = models.CharField(max_length=150, blank=True, null=False, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cost_center = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, null=True)
    project_code = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    sof_code = models.ForeignKey(SOF, on_delete=models.SET_NULL, null=True)
    dea_code = models.ForeignKey(DEA, on_delete=models.SET_NULL, null=True)
    contribution_percentage = models.IntegerField(default=100)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)

    def get_absolute_url(self):
        return reverse('users:employee-assign-project')

    def clean(self):
        if self.project_key is None:
            key = f'E{self.employee_id}C{self.cost_center_id}' + \
                  f'P{self.project_code_id}S{self.sof_code_id}D{self.dea_code_id}'
            self.project_key = key

        # validate contribution_percentage
        # to determine that no project assignment is made beyond 100% contribution per employee
        projects = EmployeeProject.objects.filter(project_key=self.project_key)
        if projects:
            total_contrib = 0
            for project in projects:
                total_contrib += project.contribution_percentage

            total_contrib += self.contribution_percentage
            if total_contrib > 100:
                total_contrib -= self.contribution_percentage
                available_contrib = 100 - total_contrib

                if available_contrib == 0:
                    raise ValidationError('No more assignments can be made to this project for this employee.')
                else:
                    raise ValidationError(f'Only {available_contrib}% contribution can be \
                     add to this project for this employee')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.employee} project'
