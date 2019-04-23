from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import Currency, PayrollCenter, Bank, EarningDeductionType, PayrollPeriod, EarningDeductionCategory
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

    # bio-data fields
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'})
    )
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(), required=True)
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all())
    image = forms.ImageField(required=False)
    mobile_number = forms.CharField(max_length=12, required=False)
    passport_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    town = forms.CharField(required=False)

    # work info fields
    duty_country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    duty_station = forms.ModelChoiceField(queryset=DutyStation.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    job_title = forms.ModelChoiceField(queryset=JobTitle.objects.all(), required=False)
    appointment_date = forms.DateField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'}),
        required=False
    )
    contract_type = forms.ModelChoiceField(queryset=ContractType.objects.all(), required=False)
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=False)
    gross_salary = forms.DecimalField(max_digits=9, decimal_places=2, required=False)
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    tin_number = forms.IntegerField(required=False)

    # payroll info fields
    social_security = forms.ChoiceField(choices=YES_OR_NO_TYPES, widget=forms.RadioSelect(), required=False)
    social_security_number = forms.ChoiceField(required=False)
    payroll_center = forms.ModelChoiceField(queryset=PayrollCenter.objects.all(), required=False)
    bank_1 = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)
    bank_2 = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)
    first_account_number = forms.IntegerField(required=False)
    second_account_number = forms.IntegerField(required=False)
    first_bank_percentage = forms.IntegerField(required=False)
    second_bank_percentage = forms.IntegerField(required=False)

    # emergency contact fields
    kin_full_name = forms.CharField(required=False)
    kin_phone_number = forms.CharField(max_length=12, required=False)
    kin_email = forms.EmailField(required=False)
    kin_relationship = forms.ModelChoiceField(queryset=Relationship.objects.all(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class ProfileUpdateForm(forms.ModelForm):
    """docstring for ProfileUpdateForm"""

    CHOICES = (
        ('APPROVED', 'Approve'),
        ('REJECTED', 'Reject'),
    )

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
        self.fields['employment_status'].label = "Change status"
        self.fields['dr_ac_code'].label = "DR A/C code"
        self.fields['cr_ac_code'].label = "CR A/C code"
        self.fields['tin_number'].label = "TIN number"

    # bio-data fields
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), disabled=True)
    id_number = forms.IntegerField(disabled=True)
    date_of_birth = forms.DateField(disabled=True)
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(), disabled=True)
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all(), disabled=True)
    image = forms.ImageField(required=False)
    mobile_number = forms.CharField(max_length=12, required=False)
    passport_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    town = forms.CharField(required=False)

    # work info fields
    duty_country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    duty_station = forms.ModelChoiceField(queryset=DutyStation.objects.all(), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    job_title = forms.ModelChoiceField(queryset=JobTitle.objects.all(), required=False)
    appointment_date = forms.DateField(disabled=True)
    contract_type = forms.ModelChoiceField(queryset=ContractType.objects.all(), required=False)
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), required=False)
    gross_salary = forms.DecimalField(max_digits=9, decimal_places=2, required=False, widget=forms.NumberInput())
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    tin_number = forms.IntegerField(required=False)

    # payroll info fields
    social_security = forms.ChoiceField(choices=YES_OR_NO_TYPES, widget=forms.RadioSelect(), required=False)
    social_security_number = forms.ChoiceField(required=False)
    payroll_center = forms.ModelChoiceField(queryset=PayrollCenter.objects.all(), required=False)
    bank_1 = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)
    bank_2 = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)
    first_account_number = forms.IntegerField(required=False)
    second_account_number = forms.IntegerField(required=False)
    first_bank_percentage = forms.IntegerField(required=False)
    second_bank_percentage = forms.IntegerField(required=False)

    # emergency contact fields
    kin_full_name = forms.CharField(required=False)
    kin_phone_number = forms.CharField(max_length=12, required=False)
    kin_email = forms.EmailField(required=False)
    kin_relationship = forms.ModelChoiceField(queryset=Relationship.objects.all(), required=False)

    employment_status = forms.ChoiceField(choices=EMP_STATUS_APP_TER, widget=forms.Select(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class EmployeeApprovalForm(ProfileUpdateForm):
    employment_status = forms.ChoiceField(choices=EMP_APPROVE_OR_REJECT, widget=forms.Select(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = '__all__'


class TerminationForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, disabled=True)
    notice_date = forms.DateTimeField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'}),
        required=False
    )
    exit_date = forms.DateTimeField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'}),
        required=False
    )
    days_given = forms.IntegerField(required=False)
    employable = forms.ChoiceField(choices=YES_OR_NO_TYPES, widget=forms.RadioSelect(), required=False)
    reason = forms.Textarea()

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
