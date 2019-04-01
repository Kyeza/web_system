from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from payroll.models import (PayrollPeriod, EarningDeductionCategory, PAYERates,
                            PayrollCenterEds, LSTRates)
from reports.models import PayrollPeriodReport
from users.models import Employee, PayrollProcessors
from .forms import (StaffCreationForm, ProfileCreationForm,
                    StaffUpdateForm, ProfileUpdateForm,
                    EmployeeApprovalForm, TerminationForm)


@login_required
def register_employee(request):
    if request.method == 'POST':
        user_creation_form = StaffCreationForm(request.POST)
        profile_creation_form = ProfileCreationForm(request.POST, request.FILES)
        if user_creation_form.is_valid() and profile_creation_form.is_valid():
            user_instance = user_creation_form.save(commit=False)
            user_instance.save()
            user_group = Group.objects.get(pk=int(request.POST.get('user_group')))
            user_group.user_set.add(user_instance)
            print(profile_creation_form.is_valid())
            user_profile_instance = profile_creation_form.save(commit=False)
            user_profile_instance.user = user_instance
            user_profile_instance.save()
            messages.success(request, 'You have successfully created a new Employee')
            return redirect('payroll:index')
    else:
        user_creation_form = StaffCreationForm()
        profile_creation_form = ProfileCreationForm()

    context = {
        'title': 'New Employee',
        'user_creation_form': user_creation_form,
        'profile_creation_form': profile_creation_form,
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    profile_user = request.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=profile_user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.employee)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Employee has been updated')
            return redirect('profile')
    else:
        user_update_form = StaffUpdateForm(instance=profile_user)
        profile_update_form = ProfileUpdateForm(instance=profile_user.employee)

    context = {
        'profile_user': profile_user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_update_profile(request, pk=None):
    prof = get_object_or_404(Employee, pk=pk)
    profile_user = prof.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=profile_user)
        print(f'User Form is valid: {user_update_form.is_valid()}')
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.employee)
        print(f'Profile Form is valid: {profile_update_form.is_valid()}')
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Employee has been updated')
            return redirect('users:edit-employee')
    else:
        user_update_form = StaffUpdateForm(instance=profile_user)
        profile_update_form = ProfileUpdateForm(instance=profile_user.employee)

    context = {
        'profile_user': profile_user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/profile.html', context)


def add_user_to_payroll_processor(user):
    user_status = user.employee.employment_status
    payroll_periods = user.employee.payroll_center.payrollperiod_set.all()
    if user_status == 'APPROVED' or user_status == 'REACTIVATED':
        if payroll_periods:
            open_payroll_period = payroll_periods.filter(status='OPEN').first()
            if open_payroll_period:
                user_payroll_center = user.employee.payroll_center
                payroll_center_ed_types = PayrollCenterEds.objects.filter(payroll_center=user_payroll_center)

                # get existing user processors if they exists
                existing_user_payroll_processors = PayrollProcessors.objects.filter(employee=user.employee) \
                    .filter(payroll_period=open_payroll_period)
                # if ed_types for the employees payroll center exit
                if payroll_center_ed_types:
                    if existing_user_payroll_processors:
                        # PayrollCenterEdTypes can change, hence in case there is one not in the processor
                        # associated with that user, then create it
                        for pc_ed_type in payroll_center_ed_types:
                            if existing_user_payroll_processors.filter(earning_and_deductions_type=pc_ed_type.ed_type):
                                # if that ed_type already has a processor associated with the user leave it and
                                # continue
                                continue
                            else:
                                # else create it
                                user_process = PayrollProcessors(employee=user.employee,
                                                                 earning_and_deductions_category=pc_ed_type.ed_type \
                                                                 .ed_category,
                                                                 earning_and_deductions_type=pc_ed_type.ed_type,
                                                                 amount=0, payroll_period=open_payroll_period)
                                user_process.save()

                    else:
                        # if its a new user in the payroll period, create processors for that user/employee
                        for pc_ed_type in payroll_center_ed_types:
                            user_process = PayrollProcessors(employee=user.employee,
                                                             earning_and_deductions_category=pc_ed_type.ed_type.ed_category,
                                                             earning_and_deductions_type=pc_ed_type.ed_type,
                                                             amount=0, payroll_period=open_payroll_period)
                            user_process.save()


@login_required
def approve_employee(request, pk=None):
    prof = get_object_or_404(Employee, pk=pk)
    profile_user = prof.user

    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=profile_user)
        print(f'User Form is valid: {user_update_form.is_valid()}')
        profile_update_form = EmployeeApprovalForm(request.POST, request.FILES, instance=profile_user.employee)
        print(f'Profile Form is valid: {profile_update_form.is_valid()}')
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            employee_profile = profile_update_form.save(commit=False)
            # change employee status to approved before saving to db and adding them to payroll processors
            employee_profile.employment_status = 'APPROVED'
            employee_profile.save()

            # add user to PayrollProcessor
            add_user_to_payroll_processor(profile_user)

            messages.success(request, 'Employee has been approved')
            return redirect('users:employee-approval')
    else:
        user_update_form = StaffUpdateForm(instance=profile_user)
        profile_update_form = EmployeeApprovalForm(instance=profile_user.employee)

    context = {
        'profile_user': profile_user,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/_approve_employee.html', context)


class RecruitedEmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'users/_recruited_employee_list.html'
    fields = [
        'marital_status', 'mobile_number', 'id_number',
        'passport_number', 'nationality', 'residential_address', 'district',
        'date_of_birth', 'sex', 'image', 'user_group',
        'duty_country', 'duty_station', 'department', 'job_title',
        'appointment_date', 'contract_type', 'cost_centre', 'grade',
        'gross_salary', 'currency', 'tin_number', 'social_security',
        'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
        'first_account_number', 'second_account_number', 'first_bank_percentage',
        'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
        'kin_relationship'
    ]
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.filter(employment_status='Recruit').order_by('-appointment_date')


class ApprovedEmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'users/_approved_employee_list.html'
    fields = [
        'marital_status', 'mobile_number', 'id_number',
        'passport_number', 'nationality', 'residential_address', 'district',
        'date_of_birth', 'sex', 'image', 'user_group',
        'duty_country', 'duty_station', 'department', 'job_title',
        'appointment_date', 'contract_type', 'cost_centre', 'grade',
        'gross_salary', 'currency', 'tin_number', 'social_security',
        'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
        'first_account_number', 'second_account_number', 'first_bank_percentage',
        'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
        'kin_relationship'
    ]
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.filter(employment_status='Approved').order_by('-appointment_date')


class TerminatedEmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'users/_terminated_employee_list.html'
    fields = [
        'marital_status', 'mobile_number', 'id_number',
        'passport_number', 'nationality', 'residential_address', 'district',
        'date_of_birth', 'sex', 'image', 'user_group',
        'duty_country', 'duty_station', 'department', 'job_title',
        'appointment_date', 'contract_type', 'cost_centre', 'grade',
        'gross_salary', 'currency', 'tin_number', 'social_security',
        'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
        'first_account_number', 'second_account_number', 'first_bank_percentage',
        'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
        'kin_relationship'
    ]
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.filter(employment_status='APPROVED').order_by('-appointment_date')


class RejectedEmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'users/_rejected_employee_list.html'
    fields = [
        'marital_status', 'mobile_number', 'id_number',
        'passport_number', 'nationality', 'residential_address', 'district',
        'date_of_birth', 'sex', 'image', 'user_group',
        'duty_country', 'duty_station', 'department', 'job_title',
        'appointment_date', 'contract_type', 'cost_centre', 'grade',
        'gross_salary', 'currency', 'tin_number', 'social_security',
        'social_security_number', 'payroll_center', 'bank_1', 'bank_2',
        'first_account_number', 'second_account_number', 'first_bank_percentage',
        'second_bank_percentage', 'kin_full_name', 'kin_phone_number', 'kin_email',
        'kin_relationship'
    ]
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.filter(employment_status='Rejected').order_by('-appointment_date')


def process_payroll_period(request, pk):
    payroll_period = get_object_or_404(PayrollPeriod, pk=pk)

    period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)
    employees_in_period = []

    # removing any terminated employees before processing
    for process in period_processes:
        if process.employee.employment_status == 'TERMINATED':
            process.delete()
        else:
            employees_in_period.append(process.employee)

    if employees_in_period:
        employees_to_process = list(set(employees_in_period))
    else:
        # redirecting to list of payroll periods in case there are no employee to process
        messages.info(request, 'There are no users in Payroll period to process')
        return redirect('payroll:open-payroll-period-list')

    earnings = EarningDeductionCategory.objects.get(pk=1)
    deductions = EarningDeductionCategory.objects.get(pk=2)
    statutory = EarningDeductionCategory.objects.get(pk=3)

    # getting updated payroll processors in case any employees have been removed
    period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)

    for employee in employees_to_process:
        gross_earnings, total_deductions, lst, paye, nssf, net_pay = 0, 0, 0, 0, 0, 0
        ge_data = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=earnings).all()

        # calculating gross earnings
        if ge_data:
            for inst in ge_data:
                if inst.earning_and_deductions_type.ed_type == 'Basic Salary':
                    inst.amount = employee.gross_salary
                    inst.save(update_fields=['amount'])
                gross_earnings += inst.amount

        # calculating LST
        fixed_lst = 0
        for lst_brac in LSTRates.objects.all():
            if int(gross_earnings) in range(int(lst_brac.lower_boundary), int(lst_brac.upper_boundary)):
                fixed_lst = lst_brac.fixed_amount / 4
                break
        lst = fixed_lst
        ge_minus_lst = gross_earnings - lst

        # calculating PAYE
        tax_bracket, tax_rate, fixed_tax = 0, 0, 0
        for tx_brac in PAYERates.objects.all():
            if int(ge_minus_lst) in range(int(tx_brac.lower_boundary), int(tx_brac.upper_boundary)):
                tax_bracket = tx_brac.lower_boundary
                tax_rate = tx_brac.rate / 100
                fixed_tax = tx_brac.fixed_amount
                break
        paye = (ge_minus_lst - tax_bracket) * tax_rate + fixed_tax

        # calculating NSSF 5% and 10%
        nssf_5 = Decimal(int(gross_earnings) * (5 / 100))
        nssf_10 = Decimal(int(gross_earnings) * (10 / 100))

        # update PAYE if exists in payroll center
        employee_paye_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type=11).first()
        if employee_paye_processor:
            employee_paye_processor.amount = paye
            employee_paye_processor.save(update_fields=['amount'])

        # update LST if exists in payroll center
        employee_lst_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type=13).first()
        if employee_paye_processor:
            employee_lst_processor.amount = lst
            employee_lst_processor.save(update_fields=['amount'])

        # update NSSF 10% if exists in payroll center
        employee_nssf_10_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type=63).first()
        if employee_nssf_10_processor:
            employee_nssf_10_processor.amount = nssf_10
            employee_nssf_10_processor.save(update_fields=['amount'])

        # update NSSF 5%_5 if exists in payroll center
        employee_nssf_5_processor = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_type=64).first()
        if employee_nssf_5_processor:
            employee_nssf_5_processor.amount = nssf_5
            employee_nssf_5_processor.save(update_fields=['amount'])

        # getting updated payroll processors with updated amounts
        period_processes = PayrollProcessors.objects.filter(payroll_period=payroll_period)

        tx_data_ded = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=deductions).all()
        tx_data_stat = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=statutory).all()

        # calculating total deductions from deductions
        if tx_data_ded:
            for inst in tx_data_ded:
                total_deductions += inst.amount

        # calculating total deductions from statutory deductions
        if tx_data_stat:
            for inst in tx_data_stat:
                total_deductions += inst.amount

        net_pay = gross_earnings - total_deductions

        report_exists = PayrollPeriodReport.objects.first(employee=employee) \
            .filter(payroll_period=payroll_period).first()

        if report_exists is None:
            user_report = PayrollPeriodReport(employee=employee,
                                              payroll_period=payroll_period,
                                              gross_earnings=gross_earnings,
                                              total_deductions=total_deductions,
                                              net_pay=net_pay)
            user_report.save()
        else:
            report_exists.gross_earnings = gross_earnings
            report_exists.total_deductions = total_deductions
            report_exists.net_pay = net_pay
            report_exists.save(update_fields=['gross_earnings', 'total_deductions', 'net_pay'])

    period_report = PayrollPeriodReport.objects.filter(payroll_period=payroll_period)
    context = {
        'payroll_period': payroll_period,
        'period_report': period_report,
    }
    return render(request, 'users/process_payroll_period.html', context)


def terminate_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = TerminationForm(instance=employee)

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'users/_terminate_employee_form.html', context)
