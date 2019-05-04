from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from payroll.models import PayrollPeriod
from users.forms import ProcessUpdateForm
from users.models import PayrollProcessors, Employee
from .forms import ReportGeneratorForm
from .models import ExTraSummaryReportInfo


@login_required
def display_summary_report(request, pk):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
    period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)
    employees_in_period = []

    # removing any terminated employees before processing
    for process in period_processes:
        if process.employee.employment_status == 'TERMINATED':
            process.delete()
        else:
            employees_in_period.append(process.employee)

    employees_to_process = list(set(employees_in_period))
    extra_reports = ExTraSummaryReportInfo.objects.all()
    context = {
        'payroll_period': payroll_period,
        'period_processes': period_processes,
        'employees_to_process': employees_to_process,
        'user_reports': extra_reports,
    }

    return render(request, 'reports/summary_report.html', context)


# noinspection PyPep8Naming
@login_required
def update_summary_report(request, pp, user):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pp)
    employee = get_object_or_404(Employee, pk=user)
    processors = PayrollProcessors.objects.filter(payroll_key__startswith=f'P{payroll_period.id}S{employee.id}')

    # Categories: earning, deductions and statutory
    cat_e = processors.filter(earning_and_deductions_category=1).all()
    cat_d = processors.filter(earning_and_deductions_category=2).all()
    cat_s = processors.filter(earning_and_deductions_category=3).all()

    extra_data = ExTraSummaryReportInfo.objects.filter(key=f'{payroll_period.payroll_key}S{employee.id}').first()

    # creating initial data for formsets
    e_data = [processor.to_dict() for processor in cat_e]
    d_data = [processor.to_dict() for processor in cat_d]
    s_data = [processor.to_dict() for processor in cat_s]

    # creating initial display formsets
    e_FormSet = formset_factory(ProcessUpdateForm, max_num=len(e_data), extra=0)
    d_FormSet = formset_factory(ProcessUpdateForm, max_num=len(d_data), extra=0)
    s_FormSet = formset_factory(ProcessUpdateForm, max_num=len(s_data), extra=0)

    if request.method == 'POST':
        e_formset = e_FormSet(request.POST, initial=e_data, prefix='earnings')
        d_formset = d_FormSet(request.POST, initial=d_data, prefix='deductions')
        s_formset = s_FormSet(request.POST, initial=s_data, prefix='statutory')

        if e_formset.is_valid() and d_formset.is_valid() and s_formset.is_valid():
            for form in e_formset:
                f = form.save(commit=False)
                f.employee = employee
                f.payroll_period = payroll_period
                f.earning_and_deductions_category_id = 1
                f.save()
            for form in d_formset:
                f = form.save(commit=False)
                f.employee = employee
                f.payroll_period = payroll_period
                f.earning_and_deductions_category_id = 2
                f.save()
            for form in s_formset:
                f = form.save(commit=False)
                f.employee = employee
                f.payroll_period = payroll_period
                f.earning_and_deductions_category_id = 3
                f.save()

            return HttpResponseRedirect(reverse('users:process_payroll-period', args=(payroll_period.id,)))

    else:
        e_formset = e_FormSet(initial=e_data, prefix='earnings')
        d_formset = d_FormSet(initial=d_data, prefix='deductions')
        s_formset = s_FormSet(initial=s_data, prefix='statutory')

    context = {
        'payroll_period': payroll_period,
        'employee': employee,
        'e_formset': e_formset,
        'd_formset': d_formset,
        's_formset': s_formset,
        'extra_data': extra_data,
    }

    return render(request, 'reports/update_summary.html', context)


def generate(payroll_periods, report):
    results = {}
    for period in payroll_periods:
        if report == 'BANK':
            processors = PayrollProcessors.objects.filter(payroll_period=period)
        elif report == 'SUMMARY':
            processors = PayrollProcessors.objects.filter(payroll_period=period)
        else:
            processors = PayrollProcessors.objects.filter(payroll_period=period) \
                .filter(Q(earning_and_deductions_type__ed_type__icontains=report)
                        | Q(earning_and_deductions_type__ed_type=report)).all()
            if report == 'PAYE':
                earnings = PayrollProcessors.objects.filter(payroll_period=period). \
                    filter(earning_and_deductions_type__ed_category=1)
                results['earnings'] = earnings

        results[period] = processors

    return results


@login_required
def generate_reports(request):
    if request.method == 'POST':
        form = ReportGeneratorForm(request.POST)
        if form.is_valid():
            payroll_center = form.cleaned_data.get('payroll_center')
            report = form.cleaned_data.get('report_type')
            year = form.cleaned_data.get('year')
            selected_month = form.cleaned_data.get('month')
            payroll_periods = payroll_center.payrollperiod_set.filter(year=year)

            data = payroll_periods.filter(month=selected_month)
            results = generate(data, report)

            earnings = None
            if 'earnings' in results.keys():
                earnings = results['earnings']
                del results['earnings']

            context = {
                'report': report,
                'results': results,
            }

            if report == 'SUMMARY' or report == 'PAYE' or report == 'BANK':
                context['user_reports'] = ExTraSummaryReportInfo.objects.all()

            if report == 'PAYE':
                context['earnings'] = earnings

            return render(request, 'reports/generated_report.html', context)
    else:
        form = ReportGeneratorForm()

    context = {
        'form': form
    }
    return render(request, 'reports/generate_report.html', context)


@login_required
def generate_payslip_report(request, pp, user):
    period = get_object_or_404(PayrollPeriod, pk=pp)
    employee = get_object_or_404(Employee, pk=user)
    proc_key = f'P{period.id}S{employee.id}'
    data = PayrollProcessors.objects.filter(payroll_key__startswith=proc_key)
    report = 'Pay Slip'
    info_key = f'{period.payroll_key}S{employee.id}'
    user_reports = ExTraSummaryReportInfo.objects.filter(key=info_key).all()

    context = {
        'report': report,
        'period': period,
        'data': data,
        'user_reports': user_reports,
    }

    return render(request, 'reports/generated_payslip_report.html', context)
