from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import PayrollCenter, PayrollPeriod


@login_required
def index(request):
    return render(request, 'payroll/index.html')


class PayrollCenterCreate(CreateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterUpdate(UpdateView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterDetailView(DetailView):
    model = PayrollCenter
    fields = ['name', 'country', 'organization', 'description']


class PayrollCenterListView(ListView):
    model = PayrollCenter
    paginate_by = 10


class PayrollPeriodCreate(CreateView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodUpdate(UpdateView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodDetailView(DetailView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodListView(ListView):
    model = PayrollPeriod
    fields = ['payroll_center', 'month', 'year', 'status']


class PayrollPeriodForProcessing(ListView):
    model = PayrollPeriod
    template_name = 'payroll/payrollperiod_process_list.html'
    fields = ['payroll_center', 'month', 'year', 'status']
    paginate_by = 10

    def get_queryset(self):
        return PayrollPeriod.objects.filter(status='OPEN').all().order_by('id')
