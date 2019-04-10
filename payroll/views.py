from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from payroll.forms import PayrollPeriodCreationForm
from .models import PayrollCenter, PayrollPeriod, EarningDeductionType, PayrollCenterEds, LSTRates, Bank, Currency


@login_required
def index(request):
    return render(request, 'payroll/index.html')


class PayrollCenterCreate(LoginRequiredMixin, CreateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Payroll Center'
        return context


class PayrollCenterUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Payroll Center'
        return context


class PayrollCenterDetailView(LoginRequiredMixin, DetailView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterListView(LoginRequiredMixin, ListView):
    model = PayrollCenter
    paginate_by = 10


class PayrollCenterStaffListView(LoginRequiredMixin, ListView):
    model = PayrollCenter
    template_name = 'payroll/payroll_center_staff_list.html'
    paginate_by = 10


class PayrollPeriodCreate(LoginRequiredMixin, CreateView):
    model = PayrollPeriod
    form_class = PayrollPeriodCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Payroll Period'
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PayrollPeriodUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Payroll Period'
        return context


class PayrollPeriodDetailView(LoginRequiredMixin, DetailView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodListView(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodCloseListView(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    template_name = 'payroll/payrollperiod_close_list.html'
    fields = ['payroll_center', 'month', 'year', 'status']
    paginate_by = 10

    def get_queryset(self):
        return PayrollPeriod.objects.filter(status="OPEN").order_by('month')


# TODO: Work on closing a Payroll Period
def close_payroll_period(request, pk):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
    print(f'{request.method} - {payroll_period.pk} - {payroll_period.payroll_center}')

    return render(request, 'payroll/modal.html', {'payroll_period': payroll_period})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Earning and Deduction'
        return context


class EarningAndDeductionUpdate(LoginRequiredMixin, UpdateView):
    model = EarningDeductionType
    fields = ['ed_type', 'description', 'ed_category', 'recurrent', 'taxable']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Earning and Deduction'
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Payroll Center Earnings and Deduction'
        return context


class PayrollCenterEdsUpdate(LoginRequiredMixin, UpdateView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Payroll Center Earning and Deduction'
        return context


class PayrollCenterEdsDetailView(LoginRequiredMixin, DetailView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']


class PayrollCenterEdsListView(LoginRequiredMixin, ListView):
    model = PayrollCenterEds
    fields = ['payroll_center', 'ed_type']
    paginate_by = 10


class LSTListView(LoginRequiredMixin, ListView):
    model = LSTRates
    fields = ['lower_boundary', 'upper_boundary', 'fixed_amount', 'rate', 'country']


class BankCreate(LoginRequiredMixin, CreateView):
    model = Bank
    fields = ['bank', 'sort_code', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Bank'
        return context


class BankUpdate(LoginRequiredMixin, UpdateView):
    model = Bank
    fields = ['bank', 'sort_code', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Bank'
        return context


class BankDetailView(LoginRequiredMixin, DetailView):
    model = Bank
    fields = ['bank', 'sort_code', 'description']


class BankListView(LoginRequiredMixin, ListView):
    model = Bank
    fields = ['bank', 'sort_code', 'description']
    paginate_by = 10


class CurrencyCreate(LoginRequiredMixin, CreateView):
    model = Currency
    fields = ['currency', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Currency'
        return context


class CurrencyUpdate(LoginRequiredMixin, UpdateView):
    model = Currency
    fields = ['currency', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Currency'
        return context


class CurrencyDetailView(LoginRequiredMixin, DetailView):
    model = Currency
    fields = ['currency', 'description']


class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    fields = ['currency', 'description']
    paginate_by = 10
