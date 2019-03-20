from django.urls import path

from .views import OrganizationCreate, OrganizationListView, OrganizationUpdate

app_name = 'support_data'
urlpatterns = [
    path('organizations/add/', OrganizationCreate.as_view(), name='organization-create'),
    path('organizations/<int:pk>/edit', OrganizationUpdate.as_view(), name='organization-update'),
    path('organizations/', OrganizationListView.as_view(), name='organization-list')
]
