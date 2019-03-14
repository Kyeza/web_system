from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('new_employee/', views.register_staff, name='new_employee'),
    path('profile/', views.profile, name='profile'),
]
