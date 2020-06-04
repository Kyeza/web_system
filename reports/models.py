from django.db import models

from payroll.models import PayrollPeriod
from users.models import Employee


class ExTraSummaryReportInfo(models.Model):
    report_id = models.CharField(max_length=150, unique=True, primary_key=True)
    payroll_period = models.ForeignKey('payroll.PayrollPeriod', on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey('users.Employee', on_delete=models.SET_NULL, related_name='report', null=True, blank=True)
    analysis = models.CharField(max_length=150, null=True, blank=True)
    staff_full_name = models.CharField(max_length=250, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-payroll_period__created_on', 'staff_full_name']
        verbose_name = 'Summary report'
        verbose_name_plural = 'Summary reports'

    def __str__(self):
        return f'{str(self.employee)}\'s SUMMARY REPORT'
