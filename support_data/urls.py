from django.urls import path

from .views import OrganizationCreate, OrganizationListView, OrganizationUpdate, OrganizationDetailView, \
    OrganizationDelete, TaxBracketCreate, TaxBracketUpdate, TaxBracketListView, TaxBracketDetailView

app_name = 'support_data'
urlpatterns = [
    path('organizations/add/', OrganizationCreate.as_view(), name='organization-create'),
    path('organization/<int:pk>/edit', OrganizationUpdate.as_view(), name='organization-update'),
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization/<int:pk>/delete/', OrganizationDelete.as_view(), name='organization-delete'),
    path('tax_bracket/add/', TaxBracketCreate.as_view(), name='tax-bracket-create'),
    path('tax_bracket<int:pk>/edit/', TaxBracketUpdate.as_view(), name='tax-bracket-update'),
    path('tax_bracket/', TaxBracketListView.as_view(), name='tax-bracket-list'),
    path('tax_bracket/<int:pk>/', TaxBracketDetailView.as_view(), name='tax-bracket-detail'),
]
