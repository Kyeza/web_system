from django.db import models
from django.urls import reverse

from payroll.models import PayrollPeriod
from users.models import Employee


class PayrollPeriodReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.SET_NULL, null=True)
    acting_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    car_transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    duty_risk_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    overtime_normal_days = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    overtime_holiday = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    income_tax_paye = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pension_fund = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    lst = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bank_loan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_advance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_arrears = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_taxable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_earning = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse('payroll:payroll-period-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.employee.user.user_name} report'
