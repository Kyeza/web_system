from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Organization, Tax


class OrganizationCreate(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationUpdate(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    fields = ['name', 'country']


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    paginate_by = 10
    ordering = 'pk'


class OrganizationDelete(LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = reverse_lazy('support_data:organization-list')


class TaxBracketCreate(LoginRequiredMixin, CreateView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']


class TaxBracketUpdate(LoginRequiredMixin, UpdateView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']


class TaxBracketDetailView(LoginRequiredMixin, DetailView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']


class TaxBracketListView(LoginRequiredMixin, ListView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']
    paginate_by = 10
