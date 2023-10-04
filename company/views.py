from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, CompanyOverview
from service.models import Service, ServiceProcess
from staff.models import Staff
from django.contrib.auth.decorators import login_required
from accounts.views import login
from accounts.models import Account
from .forms import CompanyForm, CompanyOverviewForm
from django.contrib import messages

def company(request):
    title = "About Us"
    company = Company.objects.all()[0]
    company_overview = CompanyOverview.objects.get(company=company)
    services = Service.objects.filter(company=company)
    staff = Staff.objects.filter(company=company)[:3]
    context = {
        'company': company,
        'company_overview': company_overview,
        'services': services,
        'staff': staff,
        'title': title,
    }
    return render(request, 'company/about.html', context)

@login_required(login_url = 'login')
def company_dashboard(request):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            data = Company()
            data.user = user
            data.is_client = True
            data.company_name = form.cleaned_data['company_name']
            data.website_address = form.cleaned_data['website_address']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.postal_code = form.cleaned_data['postal_code']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.logo = form.cleaned_data['logo']
            data.save()
            messages.success(request, 'Thank you! Your company has been created.')
            return redirect('company_dashboard')
    else:
        form = CompanyForm()

    context = {
        'form': form,
        'companies': companies
    }

    return render(request, 'company/company_dashboard.html', context)

@login_required(login_url = 'login')
def update_company(request, id):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)

    updated_company = get_object_or_404(Company, id=id)
    form = CompanyForm(request.POST or None, request.FILES or None, instance=updated_company)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('company_dashboard')

    context = {
        'form': form,
        'companies': companies,
        'updated_company': updated_company,
    }

    return render(request, 'company/company_dashboard.html', context)

@login_required(login_url = 'login')
def delete_company(request, id):
    deleted_company = Company.objects.get(id=id, is_client=True)
    deleted_company.delete()
    return redirect('company_dashboard')

@login_required(login_url = 'login')
def business_overview(request):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    # print(companies.values)
    business_overviews = CompanyOverview.objects.filter(company_id__in=companies)
    # print(business_overviews.values)
    if request.method == 'POST':
        form = CompanyOverviewForm(companies, request.POST)
        if form.is_valid():
            data = CompanyOverview()
            data.company = form.cleaned_data['company']
            data.business_overview = form.cleaned_data['business_overview']
            data.competive_advantage = form.cleaned_data['competive_advantage']
            data.mission_statement = form.cleaned_data['mission_statement']
            data.vision = form.cleaned_data['vision']
            data.philosophy = form.cleaned_data['philosophy']
            data.save()
            messages.success(request, 'Thank you! Your Business Overview has been created.')
            return redirect('business_overview')
    else:
        form = CompanyOverviewForm(companies)

    context = {
        'form': form,
        'business_overviews': business_overviews,
    }

    return render(request, 'company/business_overview.html', context)

@login_required(login_url = 'login')
def update_business_overview(request, id):
    user = Account.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)
    business_overviews = CompanyOverview.objects.filter(company_id__in=companies)

    updated_overview = get_object_or_404(CompanyOverview, company_id=id)
    form = CompanyOverviewForm(companies, request.POST or None, instance=updated_overview)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('business_overview')

    context = {
        'form': form,
        'business_overviews': business_overviews,
        'updated_overview': updated_overview,
    }

    return render(request, 'company/business_overview.html', context)

@login_required(login_url = 'login')
def delete_business_overview(request, id):
    deleted_overview = CompanyOverview.objects.get(id=id)
    deleted_overview.delete()
    return redirect('business_overview')
