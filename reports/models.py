from django.db import models

from payroll.models import PayrollPeriod
from users.models import Employee


class ExTraSummaryReportInfo(models.Model):
    report_id = models.CharField(max_length=150, blank=True, default=None, unique=True, primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='report')
    analysis = models.CharField(max_length=150, null=True, blank=True)
    staff_full_name = models.CharField(max_length=250, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.SET_NULL, null=True)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=None,)

    def __str__(self):
        return f'{str(self.employee)}\'s SUMMARY REPORT'
