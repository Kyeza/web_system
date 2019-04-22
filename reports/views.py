from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from payroll.models import PayrollPeriod
from users.forms import ProcessUpdateForm
from users.models import PayrollProcessors, Employee
from .forms import ReportGeneratorForm
from .models import ExTraSummaryReportInfo


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


def update_summary_report(request, pp, user):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pp)
    employee = get_object_or_404(Employee, pk=user)
    proc_key = f'P{payroll_period.id}S{employee.id}'
    processors = PayrollProcessors.objects.filter(payroll_key__startswith=proc_key)
    earnings_processors = processors.filter(earning_and_deductions_category=1).all()
    deductions_processors = processors.filter(earning_and_deductions_category=2).all()
    statutory_processors = processors.filter(earning_and_deductions_category=3).all()

    info_key = f'{payroll_period.payroll_key}S{employee.id}'
    extra_data = ExTraSummaryReportInfo.objects.filter(key=info_key).first()

    if request.method == 'POST':
        earnings_forms = [ProcessUpdateForm(request.POST, instance=form) for form in earnings_processors]
        deductions_forms = [ProcessUpdateForm(request.POST, instance=form) for form in deductions_processors]
        statutory_forms = [ProcessUpdateForm(request.POST, instance=form) for form in statutory_processors]
    else:
        earnings_forms = [ProcessUpdateForm(instance=form) for form in earnings_processors]
        deductions_forms = [ProcessUpdateForm(instance=form) for form in deductions_processors]
        statutory_forms = [ProcessUpdateForm(instance=form) for form in statutory_processors]

    context = {
        'payroll_period': payroll_period,
        'employee': employee,
        'earning_forms': earnings_forms,
        'deductions_forms': deductions_forms,
        'statutory_forms': statutory_forms,
        'extra_data': extra_data,
    }

    return render(request, 'reports/update_summary.html', context)


def generate(payroll_periods, report):
    results = {}
    for period in payroll_periods:
        if report == 'SUMMARY':
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

            if report == 'SUMMARY' or report == 'PAYE':
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
