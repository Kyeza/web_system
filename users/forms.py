from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import Currency, PayrollCenter, Bank
from support_data.models import Nationality, ContractType, Country, DutyStation, Department, JobTitle, Grade, \
    Relationship
from .constants import GENDER, MARITAL_STATUS, EMP_STATUS
from .models import Employee, User


class StaffCreationForm(UserCreationForm):
    """docstring for StaffCreationForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',
                  )


class StaffUpdateForm(forms.ModelForm):
    """docstring for StaffUpdateForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = User
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

    # bio-data fields
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
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
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False,
    )
    contract_type = forms.ModelChoiceField(queryset=ContractType.objects.all(), required=False)
    cost_centre = forms.CharField(required=False)
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
        fields = [
            'marital_status', 'mobile_number', 'id_number',
            'passport_number', 'nationality', 'residential_address', 'district',
            'date_of_birth', 'sex', 'image', 'user_group',
            'duty_country', 'duty_station', 'department', 'job_title',
            'appointment_date', 'contract_type', 'cost_centre', 'grade',
            'gross_salary', 'currency', 'tin_number', 'social_security',
            'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
            'first_account_number', 'second_account_number', 'first_bank_percentage',
            'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
            'kin_relationship'
        ]


class ProfileUpdateForm(forms.ModelForm):
    """docstring for ProfileUpdateForm"""

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
    cost_centre = forms.CharField(required=False)
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

    employment_status = forms.ChoiceField(choices=EMP_STATUS, widget=forms.Select(), required=False)

    class Meta:
        """docstring for Meta"""
        model = Employee
        fields = [
            'marital_status', 'mobile_number', 'id_number',
            'passport_number', 'nationality', 'residential_address', 'district',
            'date_of_birth', 'sex', 'image', 'user_group',
            'duty_country', 'duty_station', 'department', 'job_title',
            'appointment_date', 'contract_type', 'cost_centre', 'grade',
            'gross_salary', 'currency', 'tin_number', 'social_security',
            'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
            'first_account_number', 'second_account_number', 'first_bank_percentage',
            'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
            'kin_relationship', 'employment_status',
        ]
