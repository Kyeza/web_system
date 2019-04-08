from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import PayrollPeriodReport
from .forms import PeriodReportForm
from users.models import PayrollProcessors


def update_payroll_info(request, pk):
    report = get_object_or_404(PayrollPeriodReport, pk=pk)
    employee = report.employee
    processors = PayrollProcessors.objects.filter(employee=employee).\
        filter(payroll_period=report.payroll_period)

    if request.method == 'POST':
        form = PeriodReportForm(request.POST)
        if form.is_valid():
            valid_report = form.save(commit=False)
            valid_report.employee = employee
            valid_report.save()

            for processor in processors:
                ed_type_id = processor.earning_and_deductions_type.id

            messages.success(request, 'User successfully updated')
            return HttpResponseRedirect(
                reverse('users:process_payroll-period', kwargs={'pk': report.payroll_period.id})
            )
    else:
        form = PeriodReportForm(instance=report)

    context = {
        'employee':employee,
        'report': report,
        'form': form
    }
    return render(request, 'reports/employee_payroll_info.html', context)
