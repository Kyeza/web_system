from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from users.models import Employee
from .forms import (StaffCreationForm, ProfileCreationForm,
                    StaffUpdateForm, ProfileUpdateForm,
                    EmployeeApprovalForm)


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
            return redirect('users:employee-approval')
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
            messages.success(request, 'Employee has been updated')
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
        return Employee.objects.filter(employment_status='Terminated').order_by('-appointment_date')


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
