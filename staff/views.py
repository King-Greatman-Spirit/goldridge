from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .models import Staff
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .forms import StaffForm
from django.contrib import messages


@login_required(login_url = 'admin_login')
def staff_dashboard(request):
    # user = Account.objects.get(id=request.user.id)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all staff objects associated with the specified company (e.g., Goldridge) from the database
    staffs = Staff.objects.filter(company=company)

    if request.method == 'POST':
        form = StaffForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = Staff()
            data.company = form.cleaned_data['company']
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.job_title = form.cleaned_data['job_title']
            data.about = form.cleaned_data['about']
            data.photo = form.cleaned_data['photo']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.employment_date = form.cleaned_data['employment_date']
            data.is_management = form.cleaned_data['is_management']
            data.is_primary_contact = form.cleaned_data['is_primary_contact']
            data.save()
            messages.success(request, 'Thank you! Your Staff has been created.')
            return redirect('staff_dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    else:
        form = StaffForm(company)

    context = {
        'form': form,
        'staffs': staffs,
    }

    return render(request, 'staff/staff_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_staff(request, id):
    # user = Account.objects.get(id=request.user.id)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all staff objects associated with the specified company (e.g., Goldridge) from the database
    staffs = Staff.objects.filter(company=company)

    updated_staff = get_object_or_404(Staff, id=id)
    form = StaffForm(company, request.POST or None, request.FILES or None, instance=updated_staff)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard')

    context = {
        'form': form,
        'staffs': staffs,
        'updated_staff': updated_staff,
    }

    return render(request, 'staff/staff_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_staff(request, id):
    deleted_staff = Staff.objects.get(id=id)
    deleted_staff.delete()
    return redirect('staff_dashboard')
