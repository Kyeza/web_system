import logging
import re
import sys
from builtins import super
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from hr_system.exception import ProcessingDataError, EmptyPAYERatesTableError, EmptyLSTRatesTableError, \
    NoEmployeeInPayrollPeriodError, NoEmployeeInSystemError
from payroll.models import PayrollPeriod, PAYERates, PayrollCenterEds, LSTRates
from reports.models import ExtraSummaryReportInfo, SocialSecurityReport, TaxationReport, BankReport, LSTReport
from reports.tasks import update_or_create_user_summary_report, initialize_report_generation
from users.mixins import NeverCacheMixin
from users.models import Employee, PayrollProcessors, CostCentre, SOF, DEA, EmployeeProject, Category, Project, \
    TerminatedEmployees
from .forms import StaffCreationForm, ProfileCreationForm, StaffUpdateForm, ProfileUpdateForm, \
    EmployeeApprovalForm, TerminationForm, EmployeeProjectForm, LoginForm, ProfileGroupForm
from .utils import render_to_json

logger = logging.getLogger('payroll')


@never_cache
def login_admin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('payroll/')
            else:
                messages.warning(request, 'Invalid Username or Password!')
                return render(request, 'users/auth/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'users/auth/login.html', {'form': form})


@never_cache
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


@never_cache
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


@never_cache
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
            try:
                group = Group.objects.get(pk=request.POST.get('user_group'))
                user_profile.user_group = group
            except Group.DoesNotExist:
                logger.error(f'UserUpdateView: user {user.username} doesn\'t belong any Group.')

            user_profile.save()

            if user.groups.first():
                if user_profile.user_group:
                    if not user.groups.first() == user_profile.user_group:
                        user.groups.first().user_set.remove(user)
                        user_profile.user_group.user_set.add(user)
            else:
                if user_profile.user_group:
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


@never_cache
@login_required
@permission_required('users.can_change_user_group', raise_exception=True)
@transaction.atomic
def user_change_group(request, pk=None):
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=user)
        profile_update_form = ProfileGroupForm(request.POST, request.FILES, instance=employee)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user = user_update_form.save(commit=False)
            user.save()
            user_profile = profile_update_form.save(commit=False)

            group = Group.objects.get(pk=request.POST.get('user_group'))
            user_profile.user_group = group

            user_profile.save()

            current_user_group = user.groups.first()

            if current_user_group is not None:
                if user_profile.user_group:
                    if not user.groups.first() == user_profile.user_group:
                        user.groups.first().user_set.remove(user)
                        user_profile.user_group.user_set.add(user)
            else:
                if user_profile.user_group:
                    if user not in user_profile.user_group.user_set.all():
                        user_profile.user_group.user_set.add(user)

            logger.info(f'Employee {user.get_full_name()} has been add to user group {group}')
            messages.success(request, 'Employee\'s User group has been changed successfully')
            return redirect('payroll:index')
    else:
        user_update_form = StaffUpdateForm(instance=user)
        profile_update_form = ProfileGroupForm(instance=employee)

    context = {
        'profile_user': user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/auth/change_user_group_form.html', context)


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


class ChangeGroupEmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.can_change_user_group',)
    model = Employee
    template_name = 'users/employees/change_group_employee_list.html'

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


class SeparatedEmployeesListView(LoginRequiredMixin, NeverCacheMixin, PermissionRequiredMixin, ListView):
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


def delete_terminated_employees_reports(period_id):
    ExtraSummaryReportInfo.objects.filter(payroll_period_id=period_id, employee__employment_status='TERMINATED').delete()
    SocialSecurityReport.objects.filter(payroll_period_id=period_id, employee__employment_status='TERMINATED').delete()
    TaxationReport.objects.filter(payroll_period_id=period_id, employee__employment_status='TERMINATED').delete()
    BankReport.objects.filter(payroll_period_id=period_id, employee__employment_status='TERMINATED').delete()
    LSTReport.objects.filter(payroll_period_id=period_id, employee__employment_status='TERMINATED').delete()


def processor(payroll_period, process_lst='False', method='GET', user=None):
    logger.debug(f'started processing')
    response = {}
    payroll_center = payroll_period.payroll_center
    users = payroll_center.employee_set.all()
    employees_in_period = set()
    if users.exists() and user is None:
        logger.critical(f'Adding Payroll center users for Period {payroll_period} to processor')
        for employee in users:
            if employee.employment_status == 'APPROVED':
                inst = employee.user
                try:
                    add_user_to_payroll_processor(inst, payroll_period)
                except Exception as e:
                    logger.error(f'Something went wrong')
                    logger.error(f'{e.args}')
        logger.critical(f'Successfully added users for Period {payroll_period} to processor')
    elif user:
        employees_in_period.add(user)
    else:
        raise NoEmployeeInSystemError

    if user:
        period_processes = PayrollProcessors.objects \
            .select_related('employee', 'earning_and_deductions_type', 'earning_and_deductions_category',
                            'employee__nationality', 'employee__grade', 'employee__duty_station',
                            'employee__duty_country',
                            'employee__department', 'employee__job_title', 'employee__reports_to',
                            'employee__contract_type', 'employee__payroll_center', 'employee__bank_1',
                            'employee__bank_2',
                            'employee__category') \
            .filter(payroll_period=payroll_period).filter(employee=user) \
            .filter(payroll_period__payroll_center_id=payroll_center.id).all() \
            .prefetch_related('employee__report', 'employee__report__payroll_period')
        logger.debug(f'Processors: {period_processes.count()}')
    else:
        period_processes = PayrollProcessors.objects \
            .select_related('employee', 'earning_and_deductions_type', 'earning_and_deductions_category',
                            'employee__nationality', 'employee__grade', 'employee__duty_station',
                            'employee__duty_country',
                            'employee__department', 'employee__job_title', 'employee__reports_to',
                            'employee__contract_type', 'employee__payroll_center', 'employee__bank_1',
                            'employee__bank_2',
                            'employee__category') \
            .filter(payroll_period=payroll_period).filter(payroll_period__payroll_center_id=payroll_center.id).all() \
            .prefetch_related('employee__report', 'employee__report__payroll_period')

    # removing any terminated employees before processing
    if users.exists() and user is None:
        if period_processes.exists():
            delete_terminated_employees_reports(payroll_period.id)
            for process in period_processes.iterator():
                if process.employee.employment_status == 'TERMINATED':
                    process.delete()
                else:
                    employees_in_period.add(process.employee)
        else:
            raise NoEmployeeInPayrollPeriodError

    # getting updated payroll processors in case any employees have been removed
    # period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)
    paye_rates = PAYERates.objects.all()
    lst_rates = LSTRates.objects.all()

    employees_reports_to_generate = []
    for employee in employees_in_period:
        try:
            logger.info(f'Processing for user {employee}')
            gross_earnings, total_deductions, lst, paye, nssf, net_pay, chargeable_income = 0, 0, 0, 0, 0, 0, 0

            ge_data = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_category_id=1).all()

            # calculating gross earnings
            logger.info(f'Processing for user {employee}: calculating gross earnings')
            if ge_data.exists():
                for inst in ge_data.iterator():
                    if inst.earning_and_deductions_type.id == 1:
                        inst.amount = employee.gross_salary
                        inst.save(update_fields=['amount'])
                    elif inst.earning_and_deductions_type.id == 2 and user is None:
                        if employee.duty_station and (
                                employee.duty_station.earning_amount is not None) and inst.amount != employee.duty_station.earning_amount:
                            inst.amount = employee.duty_station.earning_amount
                            inst.save(update_fields=['amount'])
                    gross_earnings += inst.amount

            # calculating PAYE
            logger.info(f'Processing for user {employee}: calculating PAYE')
            try:
                if paye_rates.count() != 0:
                    tax_bracket, tax_rate, fixed_tax = 0, 0, 0
                    for tx_brac in paye_rates.iterator():
                        if int(gross_earnings) in range(int(tx_brac.lower_boundary), int(tx_brac.upper_boundary) + 1):
                            tax_bracket = tx_brac.lower_boundary
                            tax_rate = tx_brac.rate / 100
                            fixed_tax = tx_brac.fixed_amount
                            break
                    paye = (gross_earnings - tax_bracket) * tax_rate + fixed_tax
                    ge_minus_paye = gross_earnings - paye
                else:
                    raise EmptyPAYERatesTableError
            except EmptyPAYERatesTableError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"Payroll Processing Error: {exc_type} on line:{exc_tb.tb_lineno}")
                raise EmptyPAYERatesTableError(
                    'There are currently no PAYE rates in the system to process the Payroll, Contact IT Administrator.',
                    line_number=exc_tb.tb_lineno)

            # calculating LST
            logger.info(f'Processing for user {employee}: calculating LST')
            try:
                if lst_rates.count() != 0:
                    fixed_lst = 0
                    if process_lst == 'True':
                        if lst_rates.exists():
                            for lst_brac in lst_rates.iterator():
                                if int(ge_minus_paye) in range(int(lst_brac.lower_boundary),
                                                               int(lst_brac.upper_boundary) + 1):
                                    fixed_lst = lst_brac.fixed_amount
                                    break
                    lst = fixed_lst
                else:
                    raise EmptyLSTRatesTableError
            except EmptyLSTRatesTableError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"Payroll Processing Error: {exc_type} on line:{exc_tb.tb_lineno}")
                raise EmptyLSTRatesTableError(
                    'There are currently no LST rates in the system to process the Payroll, Contact IT Administrator.',
                    line_number=exc_tb.tb_lineno)

            # calculating the chargeable income
            chargeable_income = gross_earnings - lst

            # calculating PAYE from the chargeable income
            logger.info(f'Processing for user {employee}: calculating PAYE')
            try:
                if paye_rates.count() != 0:
                    tax_bracket, tax_rate, fixed_tax = 0, 0, 0
                    for tx_brac in paye_rates.iterator():
                        if int(chargeable_income) in range(int(tx_brac.lower_boundary), int(tx_brac.upper_boundary) + 1):
                            tax_bracket = tx_brac.lower_boundary
                            tax_rate = tx_brac.rate / 100
                            fixed_tax = tx_brac.fixed_amount
                            break
                    paye = (chargeable_income - tax_bracket) * tax_rate + fixed_tax
                else:
                    raise EmptyPAYERatesTableError
            except EmptyPAYERatesTableError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"Payroll Processing Error: {exc_type} on line:{exc_tb.tb_lineno}")
                raise EmptyPAYERatesTableError(
                    'There are currently no PAYE rates in the system to process the Payroll, Contact IT Administrator.',
                    line_number=exc_tb.tb_lineno)

            # update chargeable income
            chargeable_income_processor = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=79).first()
            if chargeable_income_processor is not None:
                chargeable_income_processor.amount = chargeable_income
                chargeable_income_processor.save(update_fields=['amount'])

            # calculating NSSF 5% and 10%
            logger.info(f'Processing for user {employee}: calculating NSSF')
            if employee.social_security == 'YES':
                nssf_5 = Decimal(int(gross_earnings) * (5 / 100))
                nssf_10 = Decimal(int(gross_earnings) * (10 / 100))
            else:
                nssf_5 = 0
                nssf_10 = 0

            # update PAYE if exists in payroll center
            logger.info(f'Processing for user {employee}: updating PAYE')
            employee_paye_processor = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=61).first()
            if employee_paye_processor:
                employee_paye_processor.amount = paye
                employee_paye_processor.save(update_fields=['amount'])

            # update LST if exists in payroll center
            logger.info(f'Processing for user {employee}: updating LST')

            employee_lst_processor = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=65).first()
            if employee_lst_processor and user is not None:
                if employee_lst_processor.amount == 0 and lst > 0:
                    employee_lst_processor.amount = lst
                    employee_lst_processor.save(update_fields=['amount'])
            elif employee_lst_processor and user is None:
                employee_lst_processor.amount = lst
                employee_lst_processor.save(update_fields=['amount'])

            # update Pension if exists in payroll center
            logger.info(f'Processing for user {employee}: updating Pension')

            employee_pension_processor = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=75).first()
            if employee_paye_processor and employee.category_id == 2:
                employee_pension_processor.amount = employee.gross_salary * Decimal(5 / 100)
                employee_pension_processor.save(update_fields=['amount'])

            # update Employer Pension if exists in payroll center
            logger.info(f'Processing for user {employee}: updating Employer Pension')
            employer_pension = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=76).first()
            arrears = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=11).first()

            employer_pension_amt = 0
            if employee.category_id == 2:
                employer_pension_amt = (employee.gross_salary + arrears.amount) / Decimal(12)

            if employer_pension:
                employer_pension.amount = employer_pension_amt
                employer_pension.save(update_fields=['amount'])

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
                .filter(earning_and_deductions_category_id=2).all()
            tx_data_stat = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_category_id=3).all()

            # calculating total deductions from deductions
            logger.info(f'Processing for user {employee}: calculating total deductions from deductions')
            if tx_data_ded.exists():
                for inst in tx_data_ded.iterator():
                    total_deductions += inst.amount

            # calculating total deductions from statutory deductions
            logger.info(f'Processing for user {employee}: calculating total deductions from statutory deductions')
            if tx_data_stat.exists():
                for inst in tx_data_stat.iterator():
                    total_deductions += inst.amount

            logger.info(f'Processing for user {employee}: calculating NET PAY')
            net_pay = gross_earnings - total_deductions

            # update net_pay if exists in payroll center
            logger.info(f'Processing for user {employee}: Net pay')
            employee_net_pay = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=60).first()
            if employee_net_pay:
                employee_net_pay.amount = net_pay
                employee_net_pay.save(update_fields=['amount'])

            # update accrued salary ap if exists in payroll center
            logger.info(f'Processing for user {employee}: Accrued Salary AP')
            employee_accrued_salary_ap = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=72).first()
            if employee_accrued_salary_ap:
                employee_accrued_salary_ap.amount = (employee.gross_salary + arrears.amount) / Decimal(12)
                employee_accrued_salary_ap.save(update_fields=['amount'])

            # update accrued salary gl if exists in payroll center
            logger.info(f'Processing for user {employee}: Accrued Salary AL')
            employee_accrued_salary_gl = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=73).first()
            if employee_accrued_salary_gl:
                employee_accrued_salary_gl.amount = (employee.gross_salary + arrears.amount) / Decimal(12)
                employee_accrued_salary_gl.save(update_fields=['amount'])

            # updating NSSF export
            logger.info(f'Processing for user {employee}: NSSF Export')
            employee_nssf_export = period_processes.filter(employee=employee) \
                .filter(earning_and_deductions_type_id=77).first()
            if employee_nssf_export:
                employee_nssf_export.amount = nssf_5 + nssf_10
                employee_nssf_export.save(update_fields=['amount'])
        except (
                EmptyPAYERatesTableError, EmptyLSTRatesTableError, NoEmployeeInPayrollPeriodError,
                NoEmployeeInSystemError):
            raise
        except Exception as err:
            print(err.args)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            raise ProcessingDataError(str(employee), exc_type, exc_tb.tb_lineno)

        user_info = {
            'employee_id': employee.pk,
            'analysis': employee.agresso_number,
            'staff_full_name': employee.user.get_full_name(),
            'job_title': employee.job_title.job_title,
            'basic_salary': employee.gross_salary,
            'payment_method': employee.payment_method,
            'duty_station': employee.duty_station.duty_station,
            'social_security_number': employee.social_security_number,
            'tin_number': employee.tin_number
        }

        period_info = {
            'period_id': payroll_period.id,
            'period': payroll_period.created_on.strftime('%B, %Y')
        }

        # create or update user reports
        update_or_create_user_summary_report(f'{payroll_period.payroll_key}S{employee.pk}', user_info, net_pay,
                                             total_deductions, gross_earnings, period_info)

        employees_reports_to_generate.append(employee.pk)

    # task to create other system reports in the background
    initialize_report_generation.delay(payroll_period.id, employees_reports_to_generate)

    logger.info(f'Finished processing {response}')

    if method == 'POST':
        logger.debug(f'Displaying report {response}')
        return response


@login_required
@transaction.atomic()
@cache_page(60 * 15)
@permission_required('payroll.process_payrollperiod', raise_exception=True)
def process_payroll_period(request, pk, user=None):
    if request.method == 'POST' and request.is_ajax():
        logger.info(f'Starting whole processing process')
        payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
        process_lst = request.POST.get('process_lst')
        try:
            response = processor(payroll_period, process_lst, 'POST')
        except ProcessingDataError as e:
            error_message = messages.error(request,
                                           f'Something went wrong while processing data for {e.args[0]}, Inform IT Administrator')
            message = render_to_string('partials/messages.html', {'error_message': error_message})
            logger.error(e.args)
            response = {'status': 'error', 'message': message}
            return render_to_json(request, response)
        except (EmptyPAYERatesTableError, EmptyLSTRatesTableError) as e:
            error_message = messages.error(request, e.args[0])
            message = render_to_string('partials/messages.html', {'error_message': error_message})
            response = {'status': 'error', 'message': message}
            return render_to_json(request, response)

        except Exception as e:
            error_message = messages.error(request,
                                           f'Something went wrong while processing payroll!, Inform IT Administrator')
            message = render_to_string('partials/messages.html', {'error_message': error_message})
            logger.error(e.args)
            response = {'status': 'error', 'message': message}
            return render_to_json(request, response)
        else:
            return JsonResponse(response)

    elif request.method == 'GET':
        payroll_period = get_object_or_404(PayrollPeriod, pk=pk)
        if user is not None:
            employee = Employee.objects.get(pk=user)
            processor(payroll_period, user=employee)
        return redirect('reports:display-summary-report', payroll_period.id)


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


@never_cache
@login_required
@permission_required('users.approve_employee', raise_exception=True)
def reactivate_employee(request, pk):
    user_profile = get_object_or_404(Employee, pk=pk)
    termination_form = TerminatedEmployees.objects.filter(employee=user_profile).first()
    if termination_form:
        termination_form.delete()
    user_profile.employment_status = 'RECRUIT'
    user_profile.save()
    messages.success(request, 'Employee successfully reactivated')
    return redirect('users:separated-employee')


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
            form.save()
            messages.success(request, f'Successfully assigned project to {employee.user.get_full_name()}')
            return redirect('users:employee-assign-project')
    else:
        form = EmployeeProjectForm(initial={'employee': employee})

    context = {
        'title': 'Assign Project',
        'form': form
    }

    return render(request, 'users/employeeproject/employeeproject_form.html', context)


class EmployeeProjectCreation(CreateView):
    model = EmployeeProject
    fields = ['employee', 'cost_center', 'project_code', 'sof_code', 'dea_code', 'contribution_percentage']
    template_name = 'users/employeeproject/employeeproject_form.html'

    def get_initial(self):
        context = super().get_initial()
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        context['employee'] = employee
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        employee = Employee.objects.get(pk=self.kwargs.get('pk'))
        project.employee = employee
        project.save()
        messages.success(self.request, f'Successfully assigned project to {employee.user.get_full_name()}')
        return redirect('users:employee-assign-project')


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
    template_name = 'users/costcentre/costcentre_detail.html'


class CostCentreListView(LoginRequiredMixin, ListView):
    model = CostCentre
    template_name = 'users/costcentre/costcentre_list.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_code', 'project_name']
    template_name = 'users/project/project_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Project'
        return context


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['project_code', 'project_name']
    template_name = 'users/project/project_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Project'
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    fields = ['project_code', 'project_name']
    template_name = 'users/project/project_detail.html'


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'users/project/project_list.html'


class SOFCreate(LoginRequiredMixin, CreateView):
    model = SOF
    fields = ['sof_code', 'sof_name']
    template_name = 'users/sof/sof_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create SOF'
        return context


class SOFUpdate(LoginRequiredMixin, UpdateView):
    model = SOF
    fields = ['sof_code', 'sof_name']
    template_name = 'users/sof/sof_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit SOF'
        return context


class SOFDetailView(LoginRequiredMixin, DetailView):
    model = SOF
    fields = ['sof_code', 'sof_name']
    template_name = 'users/sof/sof_detail.html'


class SOFListView(LoginRequiredMixin, ListView):
    model = SOF
    template_name = 'users/sof/sof_list.html'


class DEACreate(LoginRequiredMixin, CreateView):
    model = DEA
    fields = ['dea_code', 'dea_name']
    template_name = 'users/dea/dea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create DEA'
        return context


class DEAUpdate(LoginRequiredMixin, UpdateView):
    model = DEA
    fields = ['dea_code', 'dea_name']
    template_name = 'users/dea/dea_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit DEA'
        return context


class DEADetailView(LoginRequiredMixin, DetailView):
    model = DEA
    fields = ['dea_code', 'dea_name']
    template_name = 'users/dea/dea_detail.html'


class DEAListView(LoginRequiredMixin, ListView):
    model = DEA
    template_name = 'users/dea/dea_list.html'


class EmployeeProjectsDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProject
    fields = ['employee', 'cost_centre', 'project_code', 'sof_code', 'dea_code']
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
