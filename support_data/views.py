from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Organization


class OrganizationCreate(CreateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationUpdate(UpdateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationDetailView(DetailView):
    model = Organization
    fields = ['name', 'country']


class OrganizationListView(ListView):
    model = Organization
    paginate_by = 10
    ordering = 'pk'


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('support_data:organization-list')
