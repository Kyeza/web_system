from django.db import models
from django.db.models import Q
from django.utils import timezone

from payroll.models import PayrollPeriod
from users.models import Employee


class Report(models.Model):
    employee = models.ForeignKey('users.Employee', on_delete=models.SET_NULL, related_name='report', null=True,
                                 blank=True)
    report_id = models.CharField(max_length=150, unique=True, db_index=True, primary_key=True)
    payroll_period = models.ForeignKey('payroll.PayrollPeriod', on_delete=models.SET_NULL, null=True, blank=True)
    period = models.DateTimeField(default=timezone.now, null=True, blank=True)
    staff_full_name = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


class ExtraSummaryReportInfo(Report):
    analysis = models.CharField(max_length=150, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-period', 'staff_full_name']
        verbose_name = 'Summary report'
        verbose_name_plural = 'Summary reports'

    def __str__(self):
        return f'{self.staff_full_name}\'s SUMMARY REPORT'


class SocialSecurityReport(Report):
    agresso_number = models.CharField(max_length=15, null=True, blank=True)
    social_security_number = models.CharField(max_length=25, null=True, blank=True)
    duty_station = models.CharField(max_length=150, null=True, blank=True)
    job_title = models.CharField(max_length=200, null=True, blank=True)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nssf_5 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nssf_10 = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def total_social_security(self):
        return self.nssf_10 + self.nssf_5

    class Meta:
        ordering = ['-period', 'staff_full_name']
        verbose_name = 'NSSF report'
        verbose_name_plural = 'NSSF reports'

    def __str__(self):
        return f'{self.staff_full_name}\'s NSSF REPORT'


class TaxationReport(Report):
    tin_number = models.CharField(max_length=30, null=True, blank=True)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paye = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-period', 'staff_full_name']
        verbose_name = 'PAYE report'
        verbose_name_plural = 'PAYE reports'

    def __str__(self):
        return f'{self.staff_full_name}\'s PAYE REPORT'


class BankReport(Report):
    bank = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=150, null=True, blank=True)
    branch_code = models.PositiveIntegerField(null=True, blank=True)
    sort_code = models.CharField(max_length=15, null=True, blank=True)
    account_number = models.CharField(max_length=30, null=True, blank=True)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-period', 'staff_full_name']
        verbose_name = 'BANK report'
        verbose_name_plural = 'BANK reports'

    def __str__(self):
        return f'{self.staff_full_name}\'s BANK REPORT'


class LSTReport(Report):
    duty_station = models.CharField(max_length=150, null=True, blank=True)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lst = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-period', 'staff_full_name']
        verbose_name = 'LST report'
        verbose_name_plural = 'LST reports'

    def __str__(self):
        return f'{self.staff_full_name}\'s LST REPORT'
