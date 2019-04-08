from django.urls import path

from . import views
from .views import RecruitedEmployeeListView, ApprovedEmployeeListView, TerminatedEmployeeListView, \
    SeparatedEmployeesListView, RejectedEmployeeListView, EmployeeBirthdayList

app_name = 'users'
urlpatterns = [
    path('new_employee/', views.register_employee, name='new-employee'),
    path('profile/', views.profile, name='user-profile'),
    path('<int:pk>/edit_employee/', views.user_update_profile, name='user-detail'),
    path('new_employee_approval/', RecruitedEmployeeListView.as_view(), name='employee-approval'),
    path('edit_employee/', ApprovedEmployeeListView.as_view(), name='edit-employee'),
    path('terminated_employees/', TerminatedEmployeeListView.as_view(), name='terminate-employee-list'),
    path('separated_employees/', SeparatedEmployeesListView.as_view(), name='separated-employee'),
    path('rejected_employees/', RejectedEmployeeListView.as_view(), name='rejected-employee-list'),
    path('employees_birthdays/', EmployeeBirthdayList.as_view(), name='employee-birthday-list'),
    path('reject_employee/<int:pk>', views.reject_employee, name='reject-employee'),
    path('new_employee_approval/<int:pk>/edit/', views.approve_employee, name='approve-employee'),
    path('payroll_period/<int:pk>/process/', views.process_payroll_period, name='process_payroll-period'),
    path('terminate_employee/<int:pk>/', views.terminate_employee, name='terminate-employee'),
]
