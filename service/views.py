from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Service, ServiceProcess, Testimonial,
    SubServiceType, SubService, Prerequisite, Transaction
)
from company.models import Company
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .forms import ServiceForm, ServiceProcessForm, UserSubServiceForm
from django.contrib import messages


def service(request, slug):
    company = Company.objects.all()[0]
    service = Service.objects.get(company=company, slug=slug)
    title = "Service: {}".format(service.service_name)
    service_process = ServiceProcess.objects.filter(company=company, service=service).order_by('id')
    categories = []


    context = {
        'company': company,
        'services': service,
        'service_process': service_process,
        'title': title,
        'categories': categories,
    }
    return render(request, 'service/service.html', context)

@login_required(login_url = 'admin_login')
def service_dashboard(request):
    # user = Account.objects.get(id=request.user.id)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)

    if request.method == 'POST':
        form = ServiceForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = Service()
            data.company = form.cleaned_data['company']
            data.service_name = form.cleaned_data['service_name']
            data.slug = form.cleaned_data['slug']
            data.service_description = form.cleaned_data['service_description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Service has been created.')
            return redirect('service_dashboard')
        else:
            messages.error(request, 'Form submission failed. Please check the form for errors.')

    else:
        form = ServiceForm(company)

    context = {
        'form': form,
        'services': services,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service(request, id):
    # user = Account.objects.get(id=request.user.id)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)

    updated_service = get_object_or_404(Service, id=id)
    form = ServiceForm(company, request.POST or None, request.FILES or None, instance=updated_service)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('service_dashboard')

    context = {
        'form': form,
        'services': services,
        'updated_service': updated_service,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service(request, id):
    deleted_service = Service.objects.get(id=id)
    deleted_service.delete()
    return redirect('service_dashboard')

@login_required(login_url = 'admin_login')
def service_process_dashboard(request):
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)
    service_processes = ServiceProcess.objects.filter(service__in=services)

    if request.method == 'POST':
        form = ServiceProcessForm(company, request.POST, request.FILES)
        if form.is_valid():
            data = ServiceProcess()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.process_name = form.cleaned_data['process_name']
            data.process_description = form.cleaned_data['process_description']
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Thank you! Your Service Process has been created.')
            return redirect('service_process_dashboard')
    else:
        form = ServiceProcessForm(company)

    context = {
        'form': form,
        'service_processes': service_processes,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service_process(request, id):
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)
    service_processes = ServiceProcess.objects.filter(service__in=services)

    updated_sp = get_object_or_404(service_processes, id=id)
    form = ServiceProcessForm(company, request.POST or None, request.FILES or None, instance=updated_sp)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('service_process_dashboard')

    context = {
        'form': form,
        'service_processes': service_processes,
        'updated_sp': updated_sp,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service_process(request, id):
    deleted_service_processes = ServiceProcess.objects.get(id=id)
    deleted_service_processes.delete()
    return redirect('service_process_dashboard')

@login_required(login_url = 'login')
def user_subService_dashboard(request):
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)
    subServiceTypes = SubServiceType.objects.filter(service__in=services)
    subservices = SubService.objects.filter(subServiceType__in=subServiceTypes)

    if request.method == 'POST':
        form = UserSubServiceForm(company, request.POST)
        if form.is_valid():
            data = SubService()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.subServiceType = form.cleaned_data['subServiceType']
            data.user = form.cleaned_data['user']
            data.description = form.cleaned_data['description']
            data.approval = form.cleaned_data['approval']
            data.duration = form.cleaned_data['duration']
            data.rate = form.cleaned_data['rate']
            data.target = form.cleaned_data['target']
            data.save()
            messages.success(request, 'Thank you! Your User Sub-Service has been created.')
            return redirect('user_subService_dashboard')
    else:
        form = UserSubServiceForm(company)

    context = {
        'form': form,
        'subservices': subservices,
    }

    return render(request, 'service/user_subService_dashboard.html', context)



