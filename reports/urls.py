from django.urls import path

from . import views


app_name = 'reports'
urlpatterns = [
    path('payroll_report/<int:pk>', views.update_payroll_info, name='report-update')
]