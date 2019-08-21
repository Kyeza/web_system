from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone

from hr_system.constants import YES_OR_NO_TYPES
from payroll.models import EarningDeductionType
from .constants import GENDER, EMP_APPROVE_OR_REJECT
from .models import Employee, TerminatedEmployees, CostCentre, SOF, DEA, EmployeeProject, PayrollProcessors, Project


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)


class StaffCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'middle_name',
                  'email', 'password1', 'password2']


class StaffUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email',
                  )


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'])
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(), required=True)
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select(), required=True)
    appointment_date = forms.DateField(input_formats=['%Y-%m-%d'], initial=timezone.now(), required=False)
    contract_expiry = forms.DateField(input_formats=['%Y-%m-%d'], required=False)
    social_security = forms.ChoiceField(choices=YES_OR_NO_TYPES, widget=forms.RadioSelect(), required=False,
                                        initial=YES_OR_NO_TYPES[1][0])
    transferable = forms.ChoiceField(choices=YES_OR_NO_TYPES, widget=forms.RadioSelect(), required=False)


class ProfileGroupForm(forms.ModelForm):

    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = ['user_group']

    def save(self, commit=True):
        return super().save(commit)


class ProfileUpdateForm(ProfileCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_group'].widget.attrs['disabled'] = 'disabled'

    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeApprovalForm(ProfileCreationForm):

    employment_status = forms.ChoiceField(choices=EMP_APPROVE_OR_REJECT, widget=forms.Select(), required=False)

    class Meta:
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
