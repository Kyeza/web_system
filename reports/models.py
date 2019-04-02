from django.db import models

from payroll.models import PayrollPeriod
from users.models import Employee


class PayrollPeriodReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)