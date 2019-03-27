from django.urls import path

from .views import OrganizationCreate, OrganizationListView, OrganizationUpdate, OrganizationDetailView, \
    OrganizationDelete

app_name = 'support_data'
urlpatterns = [
    path('organizations/add/', OrganizationCreate.as_view(), name='organization-create'),
    path('organization/<int:pk>/edit', OrganizationUpdate.as_view(), name='organization-update'),
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization/<int:pk>/delete/', OrganizationDelete.as_view(), name='organization-delete'),
]
