from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

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
        messages.success(self.request, f'Payroll Period for {form.instance.payroll_center} month of'
                                       f' {form.instance.month} has been opened')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Payroll Periods'
        return context


class PayrollPeriodCloseListView(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    template_name = 'payroll/payrollperiod_close_list.html'
    fields = ['payroll_center', 'month', 'year', 'status']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Close Payroll Period'
        return context


def close_payroll_period(request, pk):
    if request.method == 'POST' and request.is_ajax():
        ID = request.POST.get('id')
        payroll_period = get_object_or_404(PayrollPeriod, pk=ID)
        response = JsonResponse(payroll_period.to_dict())
        return response
    else:
        payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
        payroll_period.status = 'CLOSED'
        payroll_period.save(update_fields=['status'])
        messages.success(request, f'Payroll Period for {payroll_period.payroll_center} month of'
                                  f' {payroll_period.month} has been closed') 
        return redirect('payroll:close-payroll-period-list')


class PayrollPeriodForProcessing(LoginRequiredMixin, ListView):
    model = PayrollPeriod
    template_name = 'payroll/payrollperiod_process_list.html'
    fields = ['payroll_center', 'month', 'year', 'status']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Process Payroll Period'
        return context

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
