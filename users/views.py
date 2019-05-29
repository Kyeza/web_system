import logging
import re
import time
from builtins import super
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from payroll.models import (PayrollPeriod, EarningDeductionCategory, PAYERates,
                            PayrollCenterEds, LSTRates)
from reports.models import ExTraSummaryReportInfo
from users.models import Employee, PayrollProcessors, CostCentre, Project, SOF, DEA, \
    EmployeeProject, Category
from .forms import StaffCreationForm, ProfileCreationForm, StaffUpdateForm, ProfileUpdateForm, \
    EmployeeApprovalForm, TerminationForm, EmployeeProjectForm

logger = logging.getLogger('payroll')


@login_required
@permission_required(('users.add_user', 'users.add_employee'), raise_exception=True)
@transaction.atomic
def register_employee(request):
    if request.method == 'POST':
        user_creation_form = StaffCreationForm(request.POST)
        profile_creation_form = ProfileCreationForm(request.POST, request.FILES)

        logging.getLogger('payroll').info(
            f'Is User post data valid: {user_creation_form.is_valid()} and is Profile post data \
            {profile_creation_form.is_valid()}')

        if user_creation_form.is_valid() and profile_creation_form.is_valid():
            user = user_creation_form.save(commit=False)
            user.save()
            user_profile = profile_creation_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            user_profile.user_group.user_set.add(user)

            logger.info(
                f"Employee: {user.get_full_name()} has been successful" +
                f"ly created. Employee data: {profile_creation_form.cleaned_data}")

            messages.success(request, 'You have successfully created a new Employee')
            return redirect('users:new-employee')
    else:
        user_creation_form = StaffCreationForm()
        profile_creation_form = ProfileCreationForm()

    context = {
        'title': 'New Employee',
        'user_creation_form': user_creation_form,
        'profile_creation_form': profile_creation_form,
    }
    return render(request, 'users/auth/register.html', context)


@login_required
@transaction.atomic
def profile(request):
    user = request.user
    try:
        employee = Employee.objects.get(pk=user.pk)
    except Employee.DoesNotExist:
        return redirect('payroll:index')

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=employee)

        logger.debug(f'user_form.is_valid:{user_update_form.is_valid()}')
        logger.debug(f'user_form.errors:{user_update_form.errors}')
        logger.debug(f'user_form.non_field_errors:{user_update_form.non_field_errors}')

        logger.debug(f'profile_form.is_valid:{profile_update_form.is_valid()}')
        logger.debug(f'profile_form.errors:{profile_update_form.errors}')
        logger.debug(f'profile_form.non_field_errors:{profile_update_form.non_field_errors}')

        if user_update_form.is_valid() and profile_update_form.is_valid():
            logger.info(f'Form updated')
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Employee has been updated')
            return redirect('users:user-profile')
    else:
        user_update_form = StaffUpdateForm(instance=user)
        profile_update_form = ProfileUpdateForm(instance=employee)

    context = {
        'profile_user': user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/auth/profile.html', context)


@login_required
@permission_required(('users.change_user', 'users.change_employee'), raise_exception=True)
@transaction.atomic
def user_update_profile(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=employee)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user = user_update_form.save(commit=False)
            user.save()
            user_profile = profile_update_form.save(commit=False)
            group = Group.objects.get(pk=request.POST.get('user_group'))
            user_profile.user_group = group
            user_profile.save()

            if user.groups.first():
                if user_profile.user_group:
                    if not user.groups.first() == user_profile.user_group:
                        user.groups.first().user_set.remove(user)
                        user_profile.user_group.user_set.add(user)
            else:
                if user not in user_profile.user_group.user_set.all():
                    user_profile.user_group.user_set.add(user)

            # add user to PayrollProcessor
            add_user_to_payroll_processor(user)

            messages.success(request, 'Employee has been updated')
            return redirect('users:edit-employee')
    else:
        user_update_form = StaffUpdateForm(instance=user)
        profile_update_form = ProfileUpdateForm(instance=employee, initial={'user_group': employee.user_group})

    context = {
        'profile_user': user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/auth/profile.html', context)


def add_users_for_period(payroll_period, instance):
    logger.debug(f'Adding user to Period {payroll_period}')
    user_payroll_center = instance.employee.payroll_center
    payroll_center_ed_types = PayrollCenterEds.objects.select_related('ed_type') \
        .filter(payroll_center=user_payroll_center)

    if payroll_center_ed_types.exists():
        # get existing instance processors if they exists
        existing_user_payroll_processors = PayrollProcessors.objects \
            .select_related('employee', 'earning_and_deductions_type', 'earning_and_deductions_category',
                            'payroll_period', 'earning_and_deductions_type__ed_category_id',
                            'earning_and_deductions_type__ed_type') \
            .filter(employee=instance.employee).filter(payroll_period=payroll_period)
        # if ed_types for the employees payroll center exist
        if existing_user_payroll_processors.exists():
            logger.debug(f'user\'s {payroll_period} processors exist')
            # PayrollCenterEdTypes can change, hence in case there is one not in the processor
            # associated with that instance, then create it
            for pc_ed_type in payroll_center_ed_types.iterator():
                ed_type = existing_user_payroll_processors.filter(earning_and_deductions_type=pc_ed_type.ed_type)
                if ed_type.exists():
                    # if that ed_type already has a processor associated with the instance leave
                    # it and continue
                    continue
                else:
                    # else create it
                    logger.debug(f'adding {pc_ed_type.ed_type.ed_type} to user\'s existing processors')
                    user_process = PayrollProcessors(employee=instance.employee,
                                                     earning_and_deductions_category=pc_ed_type
                                                     .ed_type.ed_category,
                                                     earning_and_deductions_type=pc_ed_type.ed_type,
                                                     amount=0, payroll_period=payroll_period)
                    user_process.save()

        else:
            logger.debug(f'Creating user\'s {payroll_period} processes in Processor')
            # if its a new instance in the payroll period, create processors for that
            # instance/employee
            for pc_ed_type in payroll_center_ed_types.iterator():
                basic_salary_reg = re.compile(r'basic salary', re.IGNORECASE, )
                hardship_allowance_reg = re.compile(r'hardship allowance', re.IGNORECASE, )
                user_process = None
                if basic_salary_reg.fullmatch(pc_ed_type.ed_type.ed_type):
                    user_process = PayrollProcessors(employee=instance.employee,
                                                     earning_and_deductions_category=pc_ed_type
                                                     .ed_type.ed_category,
                                                     earning_and_deductions_type=pc_ed_type.ed_type,
                                                     amount=instance.employee.gross_salary,
                                                     payroll_period=payroll_period)
                    logger.info(
                        f'Added {instance} {pc_ed_type.ed_type.ed_type} earning to period processes')
                elif hardship_allowance_reg.fullmatch(pc_ed_type.ed_type.ed_type):
                    if instance.employee.duty_station:
                        user_process = PayrollProcessors(employee=instance.employee,
                                                         earning_and_deductions_category=pc_ed_type
                                                         .ed_type.ed_category,
                                                         earning_and_deductions_type=pc_ed_type.ed_type,
                                                         amount=instance.employee.duty_station
                                                         .earning_amount,
                                                         payroll_period=payroll_period)
                        logger.info(
                            f'Added {instance} {pc_ed_type.ed_type.ed_type} earning to period processes')
                else:
                    user_process = PayrollProcessors(employee=instance.employee,
                                                     earning_and_deductions_category=pc_ed_type
                                                     .ed_type.ed_category,
                                                     earning_and_deductions_type=pc_ed_type.ed_type,
                                                     amount=0,
                                                     payroll_period=payroll_period)
                    logger.info(
                        f'Added {instance} {pc_ed_type.ed_type.ed_type} earning to period processes')

                if user_process:
                    user_process.save()
                else:
                    logger.error(
                        f'PayrollCenter {pc_ed_type.ed_type.ed_type} for {instance} was not processed')
    else:
        logger.error(f'Payroll center has no Earnings and Deductions')


def add_user_to_payroll_processor(instance, payroll_period=None):
    logger.debug(f'adding user: {instance} to payroll processor')
    user_status = instance.employee.employment_status
    if payroll_period:
        add_users_for_period(payroll_period, instance)
    else:
        payroll_periods = instance.employee.payroll_center.payrollperiod_set.all()
        if user_status == 'APPROVED' or user_status == 'REACTIVATED':
            if payroll_periods.exists():
                open_payroll_period = payroll_periods.filter(status='OPEN').all()
                if open_payroll_period.exists():
                    for payroll_period in open_payroll_period:
                        add_users_for_period(payroll_period, instance)
                else:
                    logger.error(f'No OPEN payroll periods in the Processor')
            else:
                logger.error(f'No PayrollPeriods in the Processor')
        else:
            logger.error(f'{instance} either not APPROVED or REACTIVATED')


@login_required
@permission_required('users.approve_employee', raise_exception=True)
def reject_employee(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk)
    employee.employment_status = 'REJECTED'
    employee.save(update_fields=['employment_status'])
    return render(request, 'users/employees/_approved_employee_list.html')


@login_required
@permission_required('users.approve_employee', raise_exception=True)
@transaction.atomic
def approve_employee(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk)
    profile_user = employee.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=profile_user)
        profile_update_form = EmployeeApprovalForm(request.POST, request.FILES, instance=employee)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            employee_profile = profile_update_form.save(commit=False)

            # change employee status to approved before saving to db and adding them to payroll processors
            employee_profile.employment_status = 'APPROVED'
            employee_profile.save()

            # add user to PayrollProcessor
            add_user_to_payroll_processor(profile_user)

            # logger.info(f'{request.user} approved Employee {employee_profile.user}')

            messages.success(request, f'{employee} has been approved')
            return redirect('users:employee-approval')
    else:
        user_update_form = StaffUpdateForm(instance=profile_user)
        profile_update_form = EmployeeApprovalForm(instance=employee)

    context = {
        'profile_user': profile_user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/employees/_approve_employee.html', context)


class RecruitedEmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.approve_employee',)
    model = Employee
    template_name = 'users/employees/_recruited_employee_list.html'

    def get_queryset(self):
        return Employee.objects.select_related('user', 'department', 'job_title') \
            .filter(employment_status='Recruit').order_by('-appointment_date').iterator()


class ApprovedEmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.change_user', 'users.change_employee')
    model = Employee

    def get_queryset(self):
        return Employee.objects \
            .select_related('user', 'nationality', 'grade', 'duty_station', 'duty_country', 'department', 'job_title',
                            'reports_to', 'contract_type', 'payroll_center', 'bank_1', 'bank_2', 'category',
                            'currency', 'kin_relationship', 'district') \
            .filter(employment_status='Approved').iterator()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Staff'
        return context


class RejectedEmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_user', 'users.view_employee')
    model = Employee
    template_name = 'users/employees/_rejected_employee_list.html'

    def get_queryset(self):
        return Employee.objects.select_related('user', 'department', 'job_title') \
            .filter(employment_status='REJECTED').iterator()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Rejected Staff'
        return context


class SeparatedEmployeesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_user', 'users.view_employee')
    model = Employee
    template_name = 'users/employees/_separated_employee_list.html'

    def get_queryset(self):
        return Employee.objects \
            .select_related('user', 'department', 'job_title').filter(employment_status='Terminated') \
            .order_by('-appointment_date').iterator()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Separated Employees'
        return context


def processor(payroll_period, process_lst='False', method='GET'):
    logger.debug(f'started processing')
    start = time.time()
    print(f'Start: {start}')
    response = {}
    users = Employee.objects.all()
    if users.exists():

        logger.critical(f'Adding users for Period {payroll_period} to processor')
        for employee in users:
            if employee.employment_status == 'APPROVED':
                user = employee.user
                try:
                    add_user_to_payroll_processor(user, payroll_period)
                except Exception as e:
                    logger.error(f'Something went wrong')
                    logger.error(f'{e.args}')
        end = time.time()
        elapsed = end - start
        print(f'End: {end}')
        print(f'Elaspsed: {elapsed}')
        logger.critical(f'Successfully added users for Period {payroll_period} to processor')
    else:
        logger.error(f'No Employees in the system')
        response['message'] = 'Something went wrong'
        response['status'] = 'Failed'

    period_processes = PayrollProcessors.objects \
        .select_related('employee', 'earning_and_deductions_type', 'earning_and_deductions_category', 'employee__nationality',
                        'employee__grade', 'employee__duty_station', 'employee__duty_country', 'employee__department', 'employee__job_title',
                        'employee__reports_to', 'employee__contract_type', 'employee__payroll_center',
                        'employee__bank_1', 'employee__bank_2', 'employee__category') \
        .filter(payroll_period=payroll_period)

    # removing any terminated employees before processing
    employees_in_period = []
    if users.exists():
        if period_processes.exists():
            for process in period_processes.iterator():
                if process.employee.employment_status == 'TERMINATED':
                    process.delete()
                else:
                    employees_in_period.append(process.employee)
        else:
            logger.error(f'Here - > There are currently no Employees for this Payroll Period')
            response['message'] = 'There are currently no Employees for this Payroll Period'
            response['status'] = 'Failed'
    else:
        logger.error(f'No Employees in the system')
    employees_to_process = list(set(employees_in_period))

    earnings = EarningDeductionCategory.objects.get(pk=1)
    deductions = EarningDeductionCategory.objects.get(pk=2)
    statutory = EarningDeductionCategory.objects.get(pk=3)

    # getting updated payroll processors in case any employees have been removed
    # period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)
    paye_rates = PAYERates.objects.all()
    lst_rates = LSTRates.objects.all()

    for employee in employees_to_process:
        logger.info(f'Processing for user {employee}')
        gross_earnings, total_deductions, lst, paye, nssf, net_pay = 0, 0, 0, 0, 0, 0
        ge_data = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=earnings).all()

        # calculating gross earnings
        logger.info(f'Processing for user {employee}: calculating gross earnings')
        if ge_data.exists():
            for inst in ge_data.iterator():
                if inst.earning_and_deductions_type.ed_type == 'Basic Salary':
                    inst.amount = employee.gross_salary
                    inst.save(update_fields=['amount'])
                elif inst.earning_and_deductions_type.ed_type.lower().__contains__('hardship'):
                    if employee.duty_station:
                        inst.amount = employee.duty_station.earning_amount
                        inst.save(update_fields=['amount'])
                gross_earnings += inst.amount

        # calculating PAYE
        logger.info(f'Processing for user {employee}: calculating PAYE')
        tax_bracket, tax_rate, fixed_tax = 0, 0, 0
        for tx_brac in paye_rates.iterator():
            if int(gross_earnings) in range(int(tx_brac.lower_boundary), int(tx_brac.upper_boundary) + 1):
                tax_bracket = tx_brac.lower_boundary
                tax_rate = tx_brac.rate / 100
                fixed_tax = tx_brac.fixed_amount
                break
        paye = (gross_earnings - tax_bracket) * tax_rate + fixed_tax
        ge_minus_paye = gross_earnings - paye

        # calculating LST
        logger.info(f'Processing for user {employee}: calculating LST')
        fixed_lst = 0
        if process_lst == 'True':
            if lst_rates.exists():
                for lst_brac in lst_rates.iterator():
                    if int(ge_minus_paye) in range(int(lst_brac.lower_boundary), int(lst_brac.upper_boundary) + 1):
                        fixed_lst = lst_brac.fixed_amount / 4
                        break
        lst = fixed_lst

        # calculating NSSF 5% and 10%
        logger.info(f'Processing for user {employee}: calculating NSSF')
        nssf_5 = Decimal(int(gross_earnings) * (5 / 100))
        nssf_10 = Decimal(int(gross_earnings) * (10 / 100))

        # update PAYE if exists in payroll center
        logger.info(f'Processing for user {employee}: updating PAYE')
        employee_paye_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type_id=61).first()
        if employee_paye_processor:
            employee_paye_processor.amount = paye
            employee_paye_processor.save(update_fields=['amount'])

        # update LST if exists in payroll center
        logger.info(f'Processing for user {employee}: updating LST')
        if process_lst == 'True':
            employee_lst_processor = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=65).first()
            if employee_paye_processor:
                employee_lst_processor.amount = lst
                employee_lst_processor.save(update_fields=['amount'])

        # update Pension if exists in payroll center
        logger.info(f'Processing for user {employee}: updating Pension')

        pension = 0
        if employee.category.pk == 1:
            pension = employee.gross_salary * (5 / 100)

        employee_pension_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type_id=75).first()
        if employee_paye_processor:
            employee_pension_processor.amount = pension
            employee_pension_processor.save(update_fields=['amount'])

        # update NSSF 10% if exists in payroll center
        logger.info(f'Processing for user {employee}: updating NSSF 10')
        employee_nssf_10_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type_id=31).first()
        if employee_nssf_10_processor:
            employee_nssf_10_processor.amount = nssf_10
            employee_nssf_10_processor.save(update_fields=['amount'])

        # update NSSF 5%_5 if exists in payroll center
        logger.info(f'Processing for user {employee}: updating NSSF 5')
        employee_nssf_5_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type_id=32).first()
        if employee_nssf_5_processor:
            employee_nssf_5_processor.amount = nssf_5
            employee_nssf_5_processor.save(update_fields=['amount'])

        tx_data_ded = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=deductions).all()
        tx_data_stat = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=statutory).all()

        # calculating total deductions from deductions
        logger.info(f'Processing for user {employee}: calculating total deductions from deductions')
        if tx_data_ded.exists():
            for inst in tx_data_ded.iterator():
                total_deductions += inst.amount

        # calculating total deductions from statutory deductions
        logger.info(f'Processing for user {employee}: calculating total deductions from statutory deductions')
        if tx_data_stat.exists():
            for inst in tx_data_stat.iterator():
                if not inst.earning_and_deductions_type.ed_type.__contains__('NSSF'):
                    total_deductions += inst.amount

        logger.info(f'Processing for user {employee}: calculating NET PAY')
        net_pay = gross_earnings - total_deductions

        try:
            key = f'{payroll_period.payroll_key}S{employee.id_number}'
            report = ExTraSummaryReportInfo.objects.get(pk=key)
            report.net_pay = net_pay
            report.gross_earning = gross_earnings
            report.total_deductions = total_deductions
            report.save(update_fields=['net_pay', 'gross_earning', 'total_deductions'])

            response['message'] = 'Successfully process Payroll Period'
            response['status'] = 'Success'
            logger.info(f'Successfully processed {employee} Payroll Period')

        except ExTraSummaryReportInfo.DoesNotExist:
            report = ExTraSummaryReportInfo(employee=employee,
                                            payroll_period=payroll_period,
                                            net_pay=net_pay,
                                            gross_earning=gross_earnings,
                                            total_deductions=total_deductions)
            report.save()

            response['message'] = 'Successfully process Payroll Period'
            response['status'] = 'Success'
            logger.info(f'Successfully processed {employee} Payroll Period')

    logger.info(f'Finished processing {response}')

    if method == 'POST':
        logger.debug(f'Displaying report {response}')
        return response


@login_required
@transaction.atomic()
@cache_page(60 * 15)
@permission_required('can.process_payrollperiod', raise_exception=True)
def process_payroll_period(request, pk):
    if request.method == 'POST' and request.is_ajax():
        logger.info(f'Starting whole processing process')
        payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
        process_lst = request.POST.get('process_lst')
        try:
            response = processor(payroll_period, process_lst, 'POST')
        except Exception as e:
            # msgs = messages.info(request, 'There are no PayrollCenter Earning and Deductions in the System')
            # html = render_to_string('partials/messages.html', {'msgs': msgs})

            logger.error(f'Something went wrong {e.args}')
            response = {'status': 'Failed', 'message': ''}
            return JsonResponse(response)
        else:
            return JsonResponse(response)

    elif request.method == 'GET':
        payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
        processor(payroll_period)
        return HttpResponseRedirect(reverse('reports:display-summary-report', args=(payroll_period.id,)))


@login_required
@permission_required('users.terminate_employee', raise_exception=True)
def terminate_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = TerminationForm(request.POST)
        if form.is_valid():
            employee.employment_status = 'TERMINATED'
            employee.save(update_fields=['employment_status'])
            instance = form.save(commit=False)
            instance.employee = employee
            instance.save()
            messages.success(request, 'Employee terminated successfully')
            return redirect('users:terminate-employee-list')
    else:
        form = TerminationForm(initial={'employee': employee})

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'users/employees/_terminate_employee_form.html', context)


class EmployeeBirthdayList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_user', 'users.view_employee')
    model = Employee
    template_name = 'users/employees/_employee_birthday_list.html'

    def get_queryset(self):
        return Employee.objects.select_related('user') \
            .filter(employment_status='APPROVED').iterator()


class AssignProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_user', 'users.view_employee')
    model = Employee
    template_name = 'users/employees/_assign_employee_project_list.html'

    def get_queryset(self):
        return Employee.objects.select_related('user', 'department', 'job_title') \
            .filter(employment_status='Approved').iterator()


@login_required
@permission_required('users.assign_employee', raise_exception=True)
def create_employee_project(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeProjectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            messages.success(request, f'Successfully assigned project to {employee.user.get_full_name()}')
            return redirect('users:employee-assign-project')
    else:
        form = EmployeeProjectForm(initial={'employee': employee})

    context = {
        'title': 'Assign Project',
        'form': form
    }

    return render(request, 'users/employeeproject/employee_project_form.html', context)


class CostCentreCreate(LoginRequiredMixin, CreateView):
    model = CostCentre
    fields = ['cost_centre', 'description']
    template_name = 'users/costcentre/costcentre_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Cost Centre'
        return context


class CostCentreUpdate(LoginRequiredMixin, UpdateView):
    model = CostCentre
    fields = ['cost_centre', 'description']
    template_name = 'users/costcentre/costcentre_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Cost Centre'
        return context


class CostCentreDetailView(LoginRequiredMixin, DetailView):
    model = CostCentre
    fields = ['cost_centre', 'description']
    template_name = 'users/costcentre/costcentre_detail.html'


class CostCentreListView(LoginRequiredMixin, ListView):
    model = CostCentre
    fields = ['cost_centre', 'description']
    template_name = 'users/costcentre/costcentre_list.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_code', 'project_name', 'cost_centre']
    template_name = 'users/project/project_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Project'
        return context


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['project_code', 'project_name', 'cost_centre']
    template_name = 'users/project/project_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Project'
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    fields = ['project_code', 'project_name', 'cost_centre']
    template_name = 'users/project/project_detail.html'


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'users/project/project_list.html'


class SOFCreate(LoginRequiredMixin, CreateView):
    model = SOF
    fields = ['sof_code', 'sof_name', 'project_code']
    template_name = 'users/sof/sof_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create SOF'
        return context


class SOFUpdate(LoginRequiredMixin, UpdateView):
    model = SOF
    fields = ['sof_code', 'sof_name', 'project_code']
    template_name = 'users/sof/sof_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit SOF'
        return context


class SOFDetailView(LoginRequiredMixin, DetailView):
    model = SOF
    fields = ['sof_code', 'sof_name', 'project_code']
    template_name = 'users/sof/sof_detail.html'


class SOFListView(LoginRequiredMixin, ListView):
    model = SOF
    template_name = 'users/sof/sof_list.html'


class DEACreate(LoginRequiredMixin, CreateView):
    model = DEA
    fields = ['dea_code', 'dea_name', 'sof_code']
    template_name = 'users/dea/dea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create DEA'
        return context


class DEAUpdate(LoginRequiredMixin, UpdateView):
    model = DEA
    fields = ['dea_code', 'dea_name', 'sof_code']
    template_name = 'users/dea/dea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit DEA'
        return context


class DEADetailView(LoginRequiredMixin, DetailView):
    model = DEA
    fields = ['dea_code', 'dea_name', 'sof_code']
    template_name = 'users/dea/dea_detail.html'


class DEAListView(LoginRequiredMixin, ListView):
    model = DEA
    template_name = 'users/dea/dea_list.html'


class EmployeeProjectsDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProject
    fields = ['employee', 'cost_centre', 'project_code', 'sof_code', 'dea_code', 'created_by']
    template_name = 'users/employeeproject/employeeproject_detail.html'


class EmployeeProjectsListView(LoginRequiredMixin, ListView):
    model = EmployeeProject
    template_name = 'users/employeeproject/employeeproject_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'users/category/category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'users/category/category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category'
        return context


class CategoryDetailView(DetailView):
    model = Category
    fields = ['name']
    template_name = 'users/category/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category'
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'users/category/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categories'
        return context
