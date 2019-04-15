import django_filters
from django.db import models
from django import forms

from users.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['user__first_name', 'user__last_name','user__email',
                  'marital_status', 'mobile_number', 'id_number',
                  'passport_number', 'nationality', 'residential_address', 'district',
                  'date_of_birth', 'sex', 'user_group',
                  'duty_country', 'duty_station', 'department', 'job_title',
                  'appointment_date', 'contract_type', 'cost_centre', 'grade',
                  'gross_salary', 'currency', 'tin_number', 'social_security',
                  'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
                  'first_account_number', 'second_account_number', 'first_bank_percentage',
                  'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
                  'kin_relationship', 'dr_ac_code', 'cr_ac_code'
                  ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }