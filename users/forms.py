from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from .users_constants import GENDER, MARITAL_STATUS, BIRTH_DATE_YEARS_RANGE
from .models import Profile, Nationality


class StaffCreationForm(UserCreationForm):
    """docstring for StaffCreationForm"""
    email = forms.EmailField()

    class Meta:
        """docstring for Meta"""
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',
                  )


class StaffUpdateForm(UserCreationForm):
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
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_DATE_YEARS_RANGE))
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all())
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
            'date_of_birth', 'sex', 'image', 'user_group',
        ]


class ProfileUpdateForm(forms.ModelForm):
    """docstring for ProfileUpdateForm"""

    def __int__(self, *args, disabled_user_group=True, disabled_sex=True, disabled_nationality=True,
                disabled_date_of_birth=True, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['sex'].disabled = disabled_sex
        self.fields['nationality'] = disabled_nationality
        self.fields['date_of_birth'] = disabled_date_of_birth
        self.fields['user_group'] = disabled_user_group

    user_group = forms.ModelChoiceField(queryset=Group.objects.all())
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_DATE_YEARS_RANGE))
    sex = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS, widget=forms.Select())
    nationality = forms.ModelChoiceField(queryset=Nationality.objects.all())
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
            'date_of_birth', 'sex', 'image', 'user_group',
        ]
