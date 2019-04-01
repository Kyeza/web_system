from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import PayrollCenter, PayrollPeriod, EarningDeductionType, PayrollCenterEds


@login_required
def index(request):
    return render(request, 'payroll/index.html')


class PayrollCenterCreate(LoginRequiredMixin, CreateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterDetailView(LoginRequiredMixin, DetailView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterListView(LoginRequiredMixin, ListView):
    model = PayrollCenter
    paginate_by = 10


class PayrollPeriodCreate(LoginRequiredMixin, CreateView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodDetailView(LoginRequiredMixin, DetailView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodListView(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodForProcessing(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    template_name = 'payroll/payrollperiod_process_list.html'
    fields = ['payroll_center', 'month', 'year', 'status']
    paginate_by = 10

    def get_queryset(self):
        return PayrollPeriod.objects.filter(status='OPEN').all().order_by('id')


class EarningAndDeductionCreate(LoginRequiredMixin, CreateView):
    model = EarningDeductionType
    fields = ['ed_type', 'description', 'ed_category', 'recurrent', 'taxable']


class EarningAndDeductionUpdate(LoginRequiredMixin, UpdateView):
    model = EarningDeductionType
    fields = ['ed_type', 'description', 'ed_category', 'recurrent', 'taxable']


class EarningAndDeductionDetailView(LoginRequiredMixin, DetailView):
    model = EarningDeductionType
    fields = ['ed_type', 'description', 'ed_category', 'recurrent', 'taxable']


class EarningAndDeductionListView(LoginRequiredMixin, ListView):
    model = EarningDeductionType
    fields = ['ed_type', 'description', 'ed_category', 'recurrent', 'taxable']
    paginate_by = 10


class PayrollCenterEdsCreate(LoginRequiredMixin, CreateView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']


class PayrollCenterEdsUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']


class PayrollCenterEdsDetailView(LoginRequiredMixin, DetailView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']


class PayrollCenterEdsListView(LoginRequiredMixin, ListView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']
    paginate_by = 10
