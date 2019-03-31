from django.urls import path

from . import views
from .views import (PayrollCenterCreate, PayrollCenterUpdate, PayrollCenterListView, PayrollCenterDetailView,
                    PayrollPeriodCreate, PayrollPeriodDetailView, PayrollPeriodListView, PayrollPeriodUpdate,
                    PayrollPeriodForProcessing)

app_name = 'payroll'
urlpatterns = [
    path('', views.index, name='index'),
    path('payroll/payroll_center/add/', PayrollCenterCreate.as_view(), name='payroll-center-create'),
    path('payroll/payroll_center/<int:pk>/edit/', PayrollCenterUpdate.as_view(), name='payroll-center-update'),
    path('payroll/payroll_center/', PayrollCenterListView.as_view(), name='payroll-center-list'),
    path('payroll/payroll_center/<int:pk>/', PayrollCenterDetailView.as_view(), name='payroll-center-detail'),
    path('payroll/payroll_period/add/', PayrollPeriodCreate.as_view(), name='payroll-period-create'),
    path('payroll/payroll_period/<int:pk>/edit/', PayrollPeriodUpdate.as_view(), name='payroll-period-update'),
    path('payroll/payroll_period/', PayrollPeriodListView.as_view(), name='payroll-period-list'),
    path('payroll/payroll_period/<int:pk>/', PayrollPeriodDetailView.as_view(), name='payroll-period-detail'),
    path('payroll/payroll_period/open', PayrollPeriodForProcessing.as_view(), name='open-payroll-period-list'),
]
