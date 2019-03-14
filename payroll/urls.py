from django.urls import path

from . import views

app_name = 'payroll'
urlpatterns = [
    path('', views.index, name='index'),
]
