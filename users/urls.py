from django.urls import path

from . import views
from .views import RecruitedEmployeeListView, ApprovedEmployeeListView, TerminatedEmployeeListView, \
    RejectedEmployeeListView

app_name = 'users'
urlpatterns = [
    path('new_employee/', views.register_employee, name='new-employee'),
    path('profile/', views.profile, name='user-profile'),
    path('<int:pk>/edit_employee/', views.user_update_profile, name='user-detail'),
    path('new_employee_approval/', RecruitedEmployeeListView.as_view(), name='employee-approval'),
    path('edit_employee/', ApprovedEmployeeListView.as_view(), name='edit-employee'),
    path('terminated_employees/', TerminatedEmployeeListView.as_view(), name='terminated-employee'),
    path('rejected_employees/', RejectedEmployeeListView.as_view(), name='rejected-employee'),
]
