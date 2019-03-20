from django.contrib import admin

from support_data.models import (Country, Nationality, DutyStation, Department, JobTitle, ContractType,
                                 Relationship, Grade, Organization, Tax)


class NationalityInline(admin.TabularInline):
    model = Nationality
    min_num = 1
    max_num = 1


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name', 'country_code']
    inlines = [NationalityInline]


admin.site.register(Country, CountryAdmin)
admin.site.register(Nationality)
admin.site.register(DutyStation)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(ContractType)
admin.site.register(Relationship)
admin.site.register(Grade)
admin.site.register(Organization)
admin.site.register(Tax)
