from datetime import datetime

from django import forms

from payroll.constants import PAYROLL_YEARS, MONTHS
from payroll.models import PayrollCenter, PayrollPeriod
from .models import ExTraSummaryReportInfo


class SummaryReportUpdateForm(forms.ModelForm):
    total_deductions = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    net_pay = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    gross_earning = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )

    class Meta:
        model = ExTraSummaryReportInfo
        fields = ['employee', 'payroll_period', 'total_deductions', 'net_pay', 'gross_earning']


class ReportGeneratorForm(forms.Form):
    REPORTS = (
        ('LST', 'LST'),
        ('NSSF', 'NSSF'),
        ('PAYE', 'PAYE'),
        ('BANK', 'Bank'),
        ('SUMMARY', 'Summary report/Pay Slip'),
    )
    _month = datetime.now().month
    payroll_center = forms.ModelChoiceField(queryset=PayrollCenter.objects.prefetch_related('payrollperiod_set').all(), widget=forms.Select())
    report_type = forms.ChoiceField(choices=REPORTS, widget=forms.Select())
    year = forms.ChoiceField(choices=PAYROLL_YEARS, widget=forms.Select())
    month = forms.ChoiceField(choices=MONTHS, widget=forms.Select(), initial=MONTHS[_month - 1][1])


class ReconciliationReportGeneratorForm(forms.Form):
    first_payroll_period = forms.ModelChoiceField(queryset=PayrollPeriod.objects.all(), widget=forms.Select())
    second_payroll_period = forms.ModelChoiceField(queryset=PayrollPeriod.objects.all(), widget=forms.Select())
