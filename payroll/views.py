from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import PayrollCenter


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
