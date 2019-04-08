from django import forms

from users.models import Employee
from .models import PayrollPeriodReport


class PeriodReportForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)
    acting_allowance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    car_transport_allowance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    duty_risk_allowance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    overtime_normal_days = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    overtime_holiday = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    housing_allowance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    bonus = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    income_tax_paye = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    pension_fund = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    lst = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    bank_loan = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    salary_advance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    salary_arrears = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    other_allowances = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    other_deductions = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    total_taxable = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    total_earning = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
    gross_salary = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right;'}
        )
    )
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

    class Meta:
        model = PayrollPeriodReport
        fields = ['employee',
                  'acting_allowance', 'car_transport_allowance', 'duty_risk_allowance',
                  'overtime_normal_days', 'overtime_holiday', 'housing_allowance',
                  'bonus', 'income_tax_paye', 'pension_fund', 'lst', 'bank_loan',
                  'salary_advance', 'salary_arrears', 'other_allowances', 'other_deductions',
                  'total_taxable', 'total_earning', 'gross_salary', 'total_deductions',
                  'net_pay'
                  ]
