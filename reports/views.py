import logging

import weasyprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import EmailMessage, get_connection
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from payroll.models import PayrollPeriod
from users.forms import ProcessUpdateForm
from users.models import PayrollProcessors, Employee
from .forms import ReportGeneratorForm, ReconciliationReportGeneratorForm
from .models import ExTraSummaryReportInfo

logger = logging.getLogger('payroll.reports')


@login_required
def display_summary_report(request, pk):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pk)

    if cache.get('summary_report') is None:
        context = generate_summary_data(payroll_period)
        cache.set('summary_report', context, 60 * 15)
        return render(request, 'reports/summary_report.html', context)
    else:
        return render(request, 'reports/summary_report.html', cache.get('summary_report'))


# generating summary data context
def generate_summary_data(payroll_period):
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

    return context


# noinspection PyPep8Naming
@login_required
def update_summary_report(request, pp, user):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pp)
    employee = get_object_or_404(Employee, pk=user)
    processors = PayrollProcessors.objects.filter(payroll_period=payroll_period).filter(employee=employee)

    # Categories: earning, deductions and statutory
    cat_e = processors.filter(earning_and_deductions_category=1).all()
    cat_d = processors.filter(earning_and_deductions_category=2).all()
    cat_s = processors.filter(earning_and_deductions_category=3).all()

    extra_data = ExTraSummaryReportInfo.objects.filter(key=f'{payroll_period.payroll_key}S{employee.pk}').first()

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


def generate(payroll_period, report):
    results = {}
    logger.info(f'generating {report} report data')
    if payroll_period:
        if report == 'BANK':
            processors = PayrollProcessors.objects.filter(payroll_period=payroll_period)
        elif report == 'SUMMARY':
            processors = PayrollProcessors.objects.filter(payroll_period=payroll_period)
        elif report == 'NSSF':
            processors = PayrollProcessors.objects.filter(
                Q(earning_and_deductions_type__ed_type__icontains='Employee NSSF')
                | Q(earning_and_deductions_type__ed_type__icontains='Employer NSSF')).all()
        else:
            processors = PayrollProcessors.objects.filter(payroll_period=payroll_period) \
                .filter(Q(earning_and_deductions_type__ed_type__icontains=report)
                        | Q(earning_and_deductions_type__ed_type=report)).all()
            if report == 'PAYE':
                earnings = PayrollProcessors.objects.filter(payroll_period=payroll_period). \
                    filter(earning_and_deductions_type__ed_category=1)
                results['earnings'] = earnings

        logger.debug(f'{report} report --> processor: {processors}')
        results[payroll_period] = processors

    logger.debug(f'{report} report --> results: {results}')
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

            payroll_period = payroll_periods.filter(month=selected_month).first()

            if payroll_period:
                if ExTraSummaryReportInfo.objects.filter(payroll_period=payroll_period):
                    logger.info(f'generating report data for {selected_month}-{year}')

                    if report == 'LST':
                        results = generate(payroll_period, 'Local Service Tax')
                    else:
                        results = generate(payroll_period, report)

                    earnings = None
                    if 'earnings' in results.keys():
                        earnings = results['earnings']
                        del results['earnings']

                    context = {
                        'title': report.capitalize() + ' Report',
                        'report': report,
                        'results': results,
                    }

                    if report == 'SUMMARY' or report == 'PAYE' or report == 'BANK' or report == 'LST':
                        context['user_reports'] = ExTraSummaryReportInfo.objects.all()

                    if report == 'PAYE':
                        context['earnings'] = earnings

                    return render(request, 'reports/generated_report.html', context)
                else:
                    logger.error(f'PayrollPeriod ({payroll_period}) not processed yet!')
                    messages.warning(request, f'PayrollPeriod ({payroll_period}) has not been processed yet!')
                    return redirect('reports:generate-reports')
            else:
                logger.error(f'PayrollPeriod ({selected_month}) doesn\' exist!')
                messages.warning(request, f'Reports for PayrollPeriod({selected_month}) don\'t exist.')
                return redirect('reports:generate-reports')



    else:
        form = ReportGeneratorForm()

    context = {
        'form': form,
        'title': 'Generate Reports'
    }
    return render(request, 'reports/generate_report.html', context)


@login_required
def generate_payslip_report(request, pp, user):
    period = get_object_or_404(PayrollPeriod, pk=pp)
    employee = get_object_or_404(Employee, pk=user)
    data = PayrollProcessors.objects.filter(payroll_period=period).filter(employee=employee)
    report = 'Pay Slip'
    info_key = f'{period.payroll_key}S{employee.pk}'
    user_reports = ExTraSummaryReportInfo.objects.filter(key=info_key).all()

    context = {
        'report': report,
        'period': period,
        'data': data,
        'user_reports': user_reports,
    }

    return render(request, 'reports/generated_payslip_report.html', context)


@login_required
def send_mass_mail(request):
    response = {}
    if request.method == 'POST':
        users = request.POST.getlist('users[]')
        period_id = request.POST.get('payroll_period')
        employees = [Employee.objects.get(id_number=int(sap_no)) for sap_no in users]
        payroll_period = get_object_or_404(PayrollPeriod, pk=int(period_id))

        emails = []
        for employee in employees:
            data = PayrollProcessors.objects.filter(payroll_period=payroll_period).filter(employee=employee)
            info_key = f'{payroll_period.payroll_key}S{employee.pk}'
            user_reports = ExTraSummaryReportInfo.objects.filter(key=info_key).all()
            context = {
                'report': 'PaySlip',
                'period': payroll_period,
                'data': data,
                'user_reports': user_reports,
            }
            html_mail = ''
            pdf = None
            try:
                html_mail = render_to_string('partials/payslip.html', context)
                pdf = weasyprint.HTML(string=html_mail).write_pdf()
            except Exception as e:
                # log
                print(e.args)

            subject = f'PAYSLIP FOR MONTH OF {payroll_period.month}'
            body = html_mail
            to = (employee.user.email,)
            email = EmailMessage(subject=subject, body=body, to=to, reply_to=['replyto@noreply.com'])
            email.content_subtype = 'html'
            email.attach('payslip.pdf', pdf, 'application/pdf')

            emails.append(email)

        connection = get_connection()
        connection.send_messages(emails)

        response = {'status': 'success'}

    return JsonResponse(response)


def get_user_processors(processors, employee):
    return processors.filter(employee=employee)


def get_category_processors(processors, category_id):
    return processors.filter(earning_and_deductions_category=category_id)


class ReconciliationUserData:

    def __init__(self, user):
        self.user = user
        self._earnings_data = {}
        self._deductions_data = {}
        self._statutory_data = {}
        self._extra_data = {}

    def add_earnings_data(self, ed_type, amount):
        self._earnings_data[ed_type] = amount

    def get_earnings_data(self):
        return self._earnings_data

    def add_deductions_data(self, ed_type, amount):
        self._deductions_data[ed_type] = amount

    def get_deductions_data(self):
        return self._deductions_data

    def add_statutory_data(self, ed_type, amount):
        self._statutory_data[ed_type] = amount

    def get_statutory_data(self):
        return self._statutory_data

    def add_extra_data(self, ed_type, amount):
        self._extra_data[ed_type] = amount

    def get_extra_data(self):
        return self._extra_data


def get_reconciled_amount(processor_1, processor_2):
    return processor_1.amount - processor_2.amount


@login_required
def generate_reconciliation_report(request):
    if request.method == 'POST':
        form = ReconciliationReportGeneratorForm(request.POST)
        if form.is_valid():
            period_one = form.cleaned_data.get('first_payroll_period')
            period_two = form.cleaned_data.get('second_payroll_period')
            context_1 = generate_summary_data(period_one)
            context_2 = generate_summary_data(period_two)

            # employees_in_both_periods
            employees_in_both_periods = set(context_1['employees_to_process']) \
                .intersection(set(context_2['employees_to_process']))

            # only in period 1
            employees_only_in_period_1 = set(context_1['employees_to_process']) \
                .difference(employees_in_both_periods)

            # only in period 2
            employees_only_in_period_2 = set(context_2['employees_to_process']) \
                .difference(employees_in_both_periods)

            reconciliation_data = []
            if employees_in_both_periods:
                for employee in employees_in_both_periods:
                    user_processors_data_1 = get_user_processors(context_1['period_processes'], employee)
                    user_processors_data_2 = get_user_processors(context_2['period_processes'], employee)
                    period_one_extra_data = ExTraSummaryReportInfo.objects.filter(
                        payroll_period=period_one).filter(employee=employee).first()
                    period_two_extra_data = ExTraSummaryReportInfo.objects.filter(
                        payroll_period=period_two).filter(employee=employee).first()

                    # earnings reconciliation
                    user_earnings_1 = get_category_processors(user_processors_data_1, 1)
                    user_earnings_2 = get_category_processors(user_processors_data_2, 1)

                    earning_set_1 = set([earning.earning_and_deductions_type for earning in user_earnings_1])
                    earning_set_2 = set([earning.earning_and_deductions_type for earning in user_earnings_2])

                    # deductions reconciliation
                    user_deductions_1 = get_category_processors(user_processors_data_1, 2)
                    user_deductions_2 = get_category_processors(user_processors_data_2, 2)

                    deductions_set_1 = set([earning.earning_and_deductions_type for earning in user_deductions_1])
                    deductions_set_2 = set([earning.earning_and_deductions_type for earning in user_deductions_2])

                    # statutory reconciliation
                    user_statutory_1 = get_category_processors(user_processors_data_1, 3)
                    user_statutory_2 = get_category_processors(user_processors_data_2, 3)

                    statutory_set_1 = set([earning.earning_and_deductions_type for earning in user_statutory_1])
                    statutory_set_2 = set([earning.earning_and_deductions_type for earning in user_statutory_2])

                    earnings_in_both = earning_set_1.intersection(earning_set_2)
                    deductions_in_both = deductions_set_1.intersection(deductions_set_2)
                    statutory_in_both = statutory_set_1.intersection(statutory_set_2)

                    user_rec_data = ReconciliationUserData(employee)
                    if earnings_in_both:
                        for earning in earnings_in_both:
                            e_processor_1 = user_earnings_1.filter(earning_and_deductions_type=earning).first()
                            e_processor_2 = user_earnings_2.filter(earning_and_deductions_type=earning).first()

                            amount = get_reconciled_amount(e_processor_1, e_processor_2)

                            user_rec_data.add_earnings_data(earning, amount)

                    if deductions_in_both:
                        for earning in deductions_in_both:
                            d_processor_1 = user_deductions_1.filter(earning_and_deductions_type=earning).first()
                            d_processor_2 = user_deductions_2.filter(earning_and_deductions_type=earning).first()

                            amount = get_reconciled_amount(d_processor_1, d_processor_2)

                            user_rec_data.add_deductions_data(earning, amount)

                    if statutory_in_both:
                        for earning in statutory_in_both:
                            s_processor_1 = user_statutory_1.filter(earning_and_deductions_type=earning).first()
                            s_processor_2 = user_statutory_2.filter(earning_and_deductions_type=earning).first()

                            amount = get_reconciled_amount(s_processor_1, s_processor_2)

                            user_rec_data.add_statutory_data(earning, amount)

                    for index in range(3):
                        if index == 0:
                            amount = period_one_extra_data.total_deductions - period_two_extra_data.total_deductions
                            user_rec_data.add_extra_data('Total Deductions', amount)
                        elif index == 1:
                            amount = period_one_extra_data.gross_earning - period_two_extra_data.gross_earning
                            user_rec_data.add_extra_data('Gross Salary', amount)
                        elif index == 2:
                            amount = period_one_extra_data.net_pay - period_two_extra_data.net_pay
                            user_rec_data.add_extra_data('Net Pay', amount)

                    reconciliation_data.append(user_rec_data)

            if employees_only_in_period_1:
                for employee in employees_only_in_period_1:
                    user_processors_data_1 = get_user_processors(context_1['period_processes'], employee)
                    period_one_extra_data = ExTraSummaryReportInfo.objects.filter(
                        payroll_period=period_one).filter(employee=employee).first()

                    # earnings reconciliation
                    user_earnings_1 = get_category_processors(user_processors_data_1, 1)

                    earning_set_1 = set([earning.earning_and_deductions_type for earning in user_earnings_1])

                    # deductions reconciliation
                    user_deductions_1 = get_category_processors(user_processors_data_1, 2)

                    deductions_set_1 = set([earning.earning_and_deductions_type for earning in user_deductions_1])

                    # statutory reconciliation
                    user_statutory_1 = get_category_processors(user_processors_data_1, 3)

                    statutory_set_1 = set([earning.earning_and_deductions_type for earning in user_statutory_1])

                    user_rec_data = ReconciliationUserData(employee)
                    if earning_set_1:
                        for earning in earning_set_1:
                            e_processor_1 = user_earnings_1.filter(earning_and_deductions_type=earning).first()

                            user_rec_data.add_earnings_data(earning, e_processor_1.amount)

                    if deductions_set_1:
                        for earning in deductions_set_1:
                            d_processor_1 = user_deductions_1.filter(earning_and_deductions_type=earning).first()

                            user_rec_data.add_deductions_data(earning, d_processor_1.amount)

                    if statutory_set_1:
                        for earning in statutory_set_1:
                            s_processor_1 = user_statutory_1.filter(earning_and_deductions_type=earning).first()
                            user_rec_data.add_statutory_data(earning, s_processor_1.amount)

                    for index in range(3):
                        if index == 0:
                            user_rec_data.add_extra_data('Total Deductions', period_one_extra_data.total_deductions)
                        elif index == 1:
                            user_rec_data.add_extra_data('Gross Salary', period_one_extra_data.gross_earning)
                        elif index == 2:
                            user_rec_data.add_extra_data('Net Pay', period_one_extra_data.net_pay)

                    reconciliation_data.append(user_rec_data)

            if employees_only_in_period_2:
                for employee in employees_only_in_period_2:
                    user_processors_data_2 = get_user_processors(context_2['period_processes'], employee)
                    period_two_extra_data = ExTraSummaryReportInfo.objects.filter(
                        payroll_period=period_two).filter(employee=employee).first()

                    # earnings reconciliation
                    user_earnings_2 = get_category_processors(user_processors_data_2, 1)

                    earning_set_2 = set([earning.earning_and_deductions_type for earning in user_earnings_2])

                    # deductions reconciliation
                    user_deductions_2 = get_category_processors(user_processors_data_2, 2)

                    deductions_set_2 = set([earning.earning_and_deductions_type for earning in user_deductions_2])

                    # statutory reconciliation
                    user_statutory_2 = get_category_processors(user_processors_data_2, 3)

                    statutory_set_2 = set([earning.earning_and_deductions_type for earning in user_statutory_2])

                    user_rec_data = ReconciliationUserData(employee)
                    if earning_set_2:
                        for earning in earning_set_2:
                            e_processor_2 = user_earnings_2.filter(earning_and_deductions_type=earning).first()

                            user_rec_data.add_earnings_data(earning, e_processor_2.amount)

                    if deductions_set_2:
                        for earning in deductions_set_2:
                            d_processor_2 = user_deductions_2.filter(earning_and_deductions_type=earning).first()

                            user_rec_data.add_earnings_data(earning, d_processor_2.amount)

                    if statutory_set_2:
                        for earning in statutory_set_2:
                            s_processor_2 = user_statutory_2.filter(earning_and_deductions_type=earning).first()

                            user_rec_data.add_earnings_data(earning, s_processor_2.amount)

                    for index in range(3):
                        if index == 0:
                            user_rec_data.add_extra_data('Total Deductions', period_two_extra_data.total_deductions)
                        elif index == 1:
                            user_rec_data.add_extra_data('Gross Salary', period_two_extra_data.gross_earning)
                        elif index == 2:
                            user_rec_data.add_extra_data('Net Pay', period_two_extra_data.net_pay)

                    reconciliation_data.append(user_rec_data)

            context = {
                'period_1': period_one,
                'period_2': period_two,
                'data': reconciliation_data
            }
            return render(request, 'reports/generated_reconciliation_report.html', context)
    else:
        form = ReconciliationReportGeneratorForm()

    context = {
        'tile': 'Reconcile Payroll Periods',
        'form': form
    }

    return render(request, 'reports/generate_reconciliation_report.html', context)
