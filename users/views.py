from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from payroll.models import (PayrollPeriod, EarningDeductionCategory, PAYERates,
                            PayrollCenterEds)
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
        open_payroll_period = PayrollPeriod.objects.filter(status='OPEN').first()
        user_payroll_center = user.employee.payroll_center
        payroll_center_ed_types = PayrollCenterEds.objects.filter(payroll_center=user_payroll_center)
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
            profile_update_form.save()

            # add user to PayrollProcessor

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
    return render(request, 'users/profile.html', context)


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
    emps_in_period = list(set([n.employee for n in period_processes]))
    earnings = EarningDeductionCategory.objects.get(pk=1)
    deductions = EarningDeductionCategory.objects.get(pk=2)
    statutory = EarningDeductionCategory.objects.get(pk=3)

    for employee in emps_in_period:
        gross_earnings, total_deductions, lst, paye, nssf, net_pay = 0, 0, 0, 0, 0, 0
        ge_data = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=earnings).all()
        tx_data_ded = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=deductions).all()
        tx_data_stat = period_processes.filter(employee=employee) \
            .filter(earning_and_deductions_category=statutory).all()

        # calculating gross earnings
        if ge_data:
            for inst in ge_data:
                gross_earnings += inst.amount

        # calculating PAYE
        tax_bracket, tax_rate, fixed_tax = 0, 0, 0
        for tx_brac in PAYERates.objects.all():
            if int(gross_earnings) in range(int(tx_brac.lower_boundary), int(tx_brac.upper_boundary)):
                tax_bracket = tx_brac.lower_boundary
                tax_rate = tx_brac.rate / 100
                fixed_tax = tx_brac.fixed_amount
                break

        paye = (gross_earnings - tax_bracket) * tax_rate + fixed_tax
        nssf = Decimal(int(gross_earnings) * (10 / 100))

        if tx_data_ded:
            for inst in tx_data_ded:
                total_deductions += inst.amount

        if tx_data_stat:
            for inst in tx_data_stat:
                total_deductions += inst.amount

        net_pay = gross_earnings - total_deductions
        user_report = PayrollPeriodReport(employee=employee,
                                          lst=lst,
                                          paye=paye,
                                          payroll_period=payroll_period,
                                          gross_earnings=gross_earnings,
                                          nssf=nssf,
                                          total_deductions=total_deductions,
                                          net_pay=net_pay)
        user_report.save()

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
