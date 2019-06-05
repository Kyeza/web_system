from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from hr_system.constants import YES_OR_NO_TYPES
from .constants import MARITAL_STATUS, GENDER, EMP_STATUS
from .utils import get_image_filename


class User(AbstractUser):

    class Meta:
        permissions = [
            ("approve_employee", "Can approve Employee"),
            ("terminate_employee", "Can terminate Employee"),
            ("assign_employee", "Can assign Project"),
        ]

    def __str__(self):
        return self.get_full_name()


class CostCentre(models.Model):
    cost_centre = models.CharField(max_length=15)
    description = models.CharField(max_length=100, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('users:cost-centre-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.cost_centre


class Category(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('users:category_list')

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, editable=False)
    user_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS, null=True)
    image = models.ImageField(default='default.png', upload_to=get_image_filename, blank=True, null=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(default=timezone.now, null=True)
    sex = models.CharField(max_length=6, choices=GENDER, null=True)
    id_number = models.CharField(max_length=200, null=True, db_index=True)
    passport_number = models.CharField(max_length=200, blank=True, null=True)
    home_address = models.CharField(max_length=200, blank=True, null=True)
    residential_address = models.CharField(max_length=200, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    tin_number = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.ForeignKey('support_data.Nationality', on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey('support_data.Grade', on_delete=models.SET_NULL, null=True, blank=True)
    duty_station = models.ForeignKey('support_data.DutyStation', on_delete=models.SET_NULL, null=True, blank=True)
    duty_country = models.ForeignKey('support_data.Country', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('support_data.Department', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.ForeignKey('support_data.JobTitle', on_delete=models.SET_NULL, null=True, blank=True)
    reports_to = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                   related_name='reports_to', null=True, blank=True)
    contract_type = models.ForeignKey('support_data.ContractType', on_delete=models.SET_NULL, null=True, blank=True)
    contract_expiry = models.DateField(null=True, blank=True)
    appointment_date = models.DateField(default=timezone.now, null=True, blank=True)
    social_security = models.CharField(max_length=3, choices=YES_OR_NO_TYPES, null=True, blank=True)
    payroll_center = models.ForeignKey('payroll.PayrollCenter', on_delete=models.SET_NULL, null=True)
    bank_1 = models.ForeignKey('payroll.Bank', on_delete=models.SET_NULL, related_name='first_bank', null=True, blank=True)
    bank_2 = models.ForeignKey('payroll.Bank', on_delete=models.SET_NULL, related_name='second_bank', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, )
    first_account_number = models.CharField(max_length=200, null=True, blank=True)
    second_account_number = models.CharField(max_length=200, null=True, blank=True)
    first_bank_percentage = models.IntegerField(null=True, blank=True, default=0)
    second_bank_percentage = models.IntegerField(null=True, blank=True, default=0)
    social_security_number = models.CharField(max_length=200, null=True, blank=True)
    currency = models.ForeignKey('payroll.Currency', on_delete=models.SET_NULL, null=True, blank=True)
    kin_full_name = models.CharField(max_length=250, null=True, blank=True)
    kin_phone_number = models.CharField(max_length=50, blank=True, null=True)
    kin_email = models.EmailField(null=True, blank=True)
    kin_relationship = models.ForeignKey('support_data.Relationship', on_delete=models.SET_NULL, null=True, blank=True)
    dr_ac_code = models.CharField(max_length=50, null=True, blank=True)
    cr_ac_code = models.CharField(max_length=50, null=True, blank=True)
    employment_status = models.CharField(max_length=17, choices=EMP_STATUS, default=EMP_STATUS[0][0], blank=True,
                                         null=True, db_index=True)
    agresso_number = models.CharField(max_length=200, null=True, blank=True, db_index=True)

    def clean(self):
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
        return f'{self.user}'


class PayrollProcessors(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    earning_and_deductions_type = models.ForeignKey('payroll.EarningDeductionType', on_delete=models.PROTECT,
                                                    blank=True, null=True)
    earning_and_deductions_category = models.ForeignKey('payroll.EarningDeductionCategory',
                                                        on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True)
    payroll_period = models.ForeignKey('payroll.PayrollPeriod', on_delete=models.SET_NULL, null=True, blank=True)
    payroll_key = models.CharField(max_length=250, blank=True, primary_key=True, unique=True, default=None,
                                   editable=False)

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
        return f'{self.employee}'


class Project(models.Model):
    project_code = models.CharField(max_length=20)
    project_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:project-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.project_code


class SOF(models.Model):
    sof_code = models.CharField(max_length=20)
    sof_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:sof-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.sof_code


class DEA(models.Model):
    dea_code = models.CharField(max_length=20)
    dea_name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('users:dea-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.dea_code


class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    cost_center = models.ForeignKey(CostCentre, on_delete=models.SET_NULL, null=True)
    project_code = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    sof_code = models.ForeignKey(SOF, on_delete=models.SET_NULL, null=True)
    dea_code = models.ForeignKey(DEA, on_delete=models.SET_NULL, null=True)
    contribution_percentage = models.IntegerField(default=100)

    def get_absolute_url(self):
        return reverse('users:employee-assign-project')

    def clean(self):
        # validate contribution_percentage
        # to determine that no project assignment is made beyond 100% contribution per employee
        projects = EmployeeProject.objects.filter(employee=self.employee, cost_center=self.cost_center_id,
                                                  project_code=self.project_code_id, sof_code=self.sof_code_id,
                                                  dea_code=self.dea_code_id)
        if projects.exists():
            total_contrib = 0
            for project in projects.iterator():
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
