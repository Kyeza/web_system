from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils import timezone

from .models import Profile


class StaffCreationForm(UserCreationForm):
    """docstring for StaffCreationForm"""
    email = forms.EmailField()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        """docstring for Meta"""
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'group'
                  ]


class StaffUpdateForm(UserCreationForm):
    """docstring for StaffUpdateForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2'
                  ]


class ProfileCreationForm(forms.ModelForm):
    """docstring for ProfileCreationForm"""
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARITAL_STATUS = (
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('SEPARATED', 'Separated'),
        ('DIVORCED', 'Divorced'),
        ('WIDOW', 'Widow')
    )

    NATIONALITY = (
        ('DJIBOUTI', 'Djibouti'),
        ('ETHIOPIAN', 'Ethiopian'),
        ('KENYAN', 'Kenyan'),
        ('SOMALI', 'Somali'),
        ('TANZANIAN', 'Tanzanian'),
        ('YEMENI', 'Yemeni'),
        ('UGANDAN', 'Ugandan'),
        ('OTHER', 'Other'),
    )

    YEARS = [year for year in range(1940, timezone.now().year)]

    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ChoiceField(choices=NATIONALITY, widget=forms.Select())
    image = forms.ImageField(required=False)
    mobile_number = forms.CharField(required=False)
    passport_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    town = forms.CharField(required=False)

    class Meta:
        """docstring for Meta"""
        model = Profile
        fields = [
            'marital_status', 'mobile_number', 'id_number',
            'passport_number', 'nationality', 'address', 'town',
            'date_of_birth', 'sex', 'image',
        ]


class ProfileUpdateForm(forms.ModelForm):
    """docstring for ProfileUpdateForm"""
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARITAL_STATUS = (
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('SEPARATED', 'Separated'),
        ('DIVORCED', 'Divorced'),
        ('WIDOW', 'Widow')
    )

    NATIONALITY = (
        ('DJIBOUTIAN', 'Djiboutian'),
        ('ETHIOPIAN', 'Ethiopian'),
        ('KENYAN', 'Kenyan'),
        ('SOMALI', 'Somali'),
        ('TANZANIAN', 'Tanzanian'),
        ('YEMENI', 'Yemeni'),
        ('UGANDAN', 'Ugandan'),
        ('OTHER', 'Other'),
    )

    YEARS = [year for year in range(1940, timezone.now().year)]

    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ChoiceField(choices=NATIONALITY, widget=forms.Select())
    image = forms.ImageField(required=False)
    mobile_number = forms.CharField(required=False)
    passport_number = forms.CharField(required=False)
    address = forms.CharField(required=False)
    town = forms.CharField(required=False)

    class Meta:
        """docstring for Meta"""
        model = Profile
        fields = [
            'marital_status', 'mobile_number', 'id_number',
            'passport_number', 'nationality', 'address', 'town',
            'date_of_birth', 'sex', 'image',
        ]
