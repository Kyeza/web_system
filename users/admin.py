from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.get_fields() if str(field).startswith('users.Employee.')]


admin.site.register(User, UserAdmin)
admin.site.register(Employee, EmployeeAdmin)
