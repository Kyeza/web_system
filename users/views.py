from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group

from users.models import Profile
from .forms import StaffCreationForm, ProfileCreationForm, StaffUpdateForm, ProfileUpdateForm


@login_required
def register_staff(request):
    if request.method == 'POST':
        user_creation_form = StaffCreationForm(request.POST)
        profile_creation_form = ProfileCreationForm(request.POST, request.FILES)
        if user_creation_form.is_valid() and profile_creation_form.is_valid():
            user_instance = user_creation_form.save(commit=False)
            user_instance.save()
            user_group = Group.objects.get(pk=int(request.POST.get('user_group')))
            user_group.user_set.add(user_instance)
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
    if request.method == 'POST':
        user_update_form = StaffUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('profile')
    else:
        user_update_form = StaffUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/profile.html', context)
