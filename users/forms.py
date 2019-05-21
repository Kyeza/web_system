from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import Currency, PayrollCenter, Bank, EarningDeductionType
from support_data.models import Nationality, ContractType, Country, DutyStation, Department, JobTitle, Grade, \
    Relationship
from .constants import GENDER, MARITAL_STATUS, EMP_STATUS_APP_TER, EMP_APPROVE_OR_REJECT
from .models import Employee, TerminatedEmployees, CostCentre, Project, SOF, DEA, EmployeeProject, PayrollProcessors


class StaffCreationForm(UserCreationForm):
    """docstring for StaffCreationForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',
                  )


class StaffUpdateForm(forms.ModelForm):
    """docstring for StaffUpdateForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email',
                  )


class ProfileCreationForm(forms.ModelForm):
    """docstring for ProfileCreationForm"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_account_number'].label = "Account Number 1"
        self.fields['second_account_number'].label = "Account Number 2"
        self.fields['first_bank_percentage'].label = "Percentage"
        self.fields['second_bank_percentage'].label = "Percentage"
        self.fields['kin_full_name'].label = "Full name"
        self.fields['kin_email'].label = "Email"
        self.fields['kin_phone_number'].label = "Phone"
        self.fields['kin_relationship'].label = "Relationship"
        self.fields['dr_ac_code'].label = "DR A/C code"
        self.fields['cr_ac_code'].label = "CR A/C code"
        self.fields['tin_number'].label = "TIN number"

    date_of_birth = forms.DateField(
        input_formats=['%Y-%m-%d']
    )
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(), required=True)
    appointment_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        initial=timezone.now(),
        required=False
    )
    contract_expiry = forms.DateField(
        input_formats=['%Y-%m-%d'],
        required=False
    )

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class ProfileUpdateForm(ProfileCreationForm):
    """docstring for ProfileUpdateForm"""

    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class EmployeeApprovalForm(ProfileCreationForm):
    """docstring for EmployeeApprovalForm"""

    employment_status = forms.ChoiceField(choices=EMP_APPROVE_OR_REJECT, widget=forms.Select(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class TerminationForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
    notice_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        required=False
    )
    exit_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        required=False
    )

    class Meta:
        model = TerminatedEmployees
        fields = '__all__'


class EmployeeProjectForm(forms.ModelForm):
    class Meta:
        model = EmployeeProject
        fields = '__all__'


class CostCentreForm(forms.ModelForm):
    class Meta:
        model = CostCentre
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class SOFForm(forms.ModelForm):
    class Meta:
        model = SOF
        fields = '__all__'


class DEAForm(forms.ModelForm):
    class Meta:
        model = DEA

        fields = '__all__'


class ProcessUpdateForm(forms.ModelForm):
    earning_and_deductions_type = forms.ModelChoiceField(
        queryset=EarningDeductionType.objects.all(),
        widget=forms.Select(
            attrs={
                'style':
                    'border: none; outline: none; text-align: left; margin: 0;' +
                    '-webkit-appearance: none; -moz-appearance: none;' +
                    'text-indent: 1px; text-overflow: \' \'; background-color: transparent;',
            }
        ),
        required=False
    )
    amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'style': 'border: none; outline: none; text-align: right; margin: 0;'}
        )
    )

    class Meta:
        model = PayrollProcessors
        exclude = ['employee', 'payroll_period', 'earning_and_deductions_category']
