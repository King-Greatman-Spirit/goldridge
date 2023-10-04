from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceProcess
from company.models import Company
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .forms import ServiceForm, ServiceProcessForm
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

@login_required(login_url = 'login')
def service_dashboard(request):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    services = Service.objects.filter(company_id__in=companies)

    if request.method == 'POST':
        form = ServiceForm(companies, request.POST, request.FILES)
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
        form = ServiceForm(companies)

    context = {
        'form': form,
        'services': services,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'login')
def update_service(request, id):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    services = Service.objects.filter(company_id__in=companies)

    updated_service = get_object_or_404(Service, id=id)
    form = ServiceForm(companies, request.POST or None, request.FILES or None, instance=updated_service)

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

@login_required(login_url = 'login')
def delete_service(request, id):
    deleted_service = Service.objects.get(id=id)
    deleted_service.delete()
    return redirect('service_dashboard')

@login_required(login_url = 'login')
def service_process_dashboard(request):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    services = Service.objects.filter(company_id__in=companies)
    service_processes = ServiceProcess.objects.filter(service_id__in=services)

    if request.method == 'POST':
        form = ServiceProcessForm(companies, request.POST, request.FILES)
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
        form = ServiceProcessForm(companies)

    context = {
        'form': form,
        'service_processes': service_processes,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'login')
def update_service_process(request, id):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    services = Service.objects.filter(company_id__in=companies)
    service_processes = ServiceProcess.objects.filter(service_id__in=services)

    updated_sp = get_object_or_404(service_processes, id=id)
    form = ServiceProcessForm(companies, request.POST or None, request.FILES or None, instance=updated_sp)

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

@login_required(login_url = 'login')
def delete_service_process(request, id):
    deleted_service_processes = ServiceProcess.objects.get(id=id)
    deleted_service_processes.delete()
    return redirect('service_process_dashboard')
