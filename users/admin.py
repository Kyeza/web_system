from django.contrib import admin

from .models import Profile, Country, Nationality


class NationalityInline(admin.TabularInline):
    model = Nationality
    min_num = 1
    max_num = 1


class CountryAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = [NationalityInline]


admin.site.register(Profile)
admin.site.register(Country, CountryAdmin)
