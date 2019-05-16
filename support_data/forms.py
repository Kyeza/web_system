from django import forms

from .models import DutyStation


class DutyStationCreationForm(forms.ModelForm):

    class Meta:
        model = DutyStation
        fields = '__all__'