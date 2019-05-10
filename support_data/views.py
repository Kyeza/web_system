from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Organization, Tax, Country, Nationality, DutyStation, Department, JobTitle, ContractType, Grade


class OrganizationCreate(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name', 'country']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Organization'
        return context


class OrganizationUpdate(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'country']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Organization'
        return context


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    fields = ['name', 'country']


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    ordering = 'pk'


class OrganizationDelete(LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = reverse_lazy('support_data:organization-list')


class TaxBracketCreate(LoginRequiredMixin, CreateView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Tax Bracket'
        return context


class TaxBracketUpdate(LoginRequiredMixin, UpdateView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Tax Bracket'
        return context


class TaxBracketDetailView(LoginRequiredMixin, DetailView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']


class TaxBracketListView(LoginRequiredMixin, ListView):
    model = Tax
    fields = ['country', 'lower_boundary', 'upper_boundary', 'fixed_amount', 'year']


class CountryOriginCreate(LoginRequiredMixin, CreateView):
    model = Country
    fields = ['country_name', 'country_code']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Country of Origin'
        return context


class CountryOriginUpdate(LoginRequiredMixin, UpdateView):
    model = Country
    fields = ['country_name', 'country_code']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Country of Origin'
        return context


class CountryOriginDetailView(LoginRequiredMixin, DetailView):
    model = Country
    fields = ['country_name', 'country_code']


class CountryOriginListView(LoginRequiredMixin, ListView):
    model = Country
    fields = ['country_name', 'country_code']


class NationalityCreate(LoginRequiredMixin, CreateView):
    model = Nationality
    fields = ['country', 'country_nationality']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Nationality'
        return context


class NationalityUpdate(LoginRequiredMixin, UpdateView):
    model = Nationality
    fields = ['country', 'country_nationality']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Nationality'
        return context


class NationalityDetailView(LoginRequiredMixin, DetailView):
    model = Nationality
    fields = ['country', 'country_nationality']


class NationalityListView(LoginRequiredMixin, ListView):
    model = Nationality
    fields = ['country', 'country_nationality']


class DutyStationCreate(LoginRequiredMixin, CreateView):
    model = DutyStation
    fields = ['duty_station', 'description', 'country']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Duty Station'
        return context


class DutyStationUpdate(LoginRequiredMixin, UpdateView):
    model = DutyStation
    fields = ['duty_station', 'description', 'country']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Duty Station'
        return context


class DutyStationDetailView(LoginRequiredMixin, DetailView):
    model = DutyStation
    fields = ['duty_station', 'description', 'country']


class DutyStationListView(LoginRequiredMixin, ListView):
    model = DutyStation
    fields = ['duty_station', 'description', 'country']


class DepartmentCreate(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['department', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Department'
        return context


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ['department', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Department'
        return context


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    fields = ['department', 'description']


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    fields = ['department', 'description']


class JobTitleCreate(LoginRequiredMixin, CreateView):
    model = JobTitle
    fields = ['job_title', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Job Title'
        return context


class JobTitleUpdate(LoginRequiredMixin, UpdateView):
    model = JobTitle
    fields = ['job_title', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Job Title'
        return context


class JobTitleDetailView(LoginRequiredMixin, DetailView):
    model = JobTitle
    fields = ['job_title', 'description']


class JobTitleListView(LoginRequiredMixin, ListView):
    model = JobTitle
    fields = ['job_title', 'description']


class ContractTypeCreate(LoginRequiredMixin, CreateView):
    model = ContractType
    fields = ['contract_type', 'contract_expiry', 'leave_entitled', 'leave_days_entitled']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Contract Type'
        return context


class ContractTypeUpdate(LoginRequiredMixin, UpdateView):
    model = ContractType
    fields = ['contract_type', 'contract_expiry', 'leave_entitled', 'leave_days_entitled']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Contract Type'
        return context


class ContractTypeDetailView(LoginRequiredMixin, DetailView):
    model = ContractType
    fields = ['contract_type', 'contract_expiry', 'leave_entitled', 'leave_days_entitled']


class ContractTypeListView(LoginRequiredMixin, ListView):
    model = ContractType
    fields = ['contract_type', 'contract_expiry', 'leave_entitled', 'leave_days_entitled']


class GradeCreate(LoginRequiredMixin, CreateView):
    model = Grade
    fields = ['grade', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Grade'
        return context


class GradeUpdate(LoginRequiredMixin, UpdateView):
    model = Grade
    fields = ['grade', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Grade'
        return context


class GradeDetailView(LoginRequiredMixin, DetailView):
    model = Grade
    fields = ['grade', 'description']


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    fields = ['grade', 'description']
