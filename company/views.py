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
    return render(request, 'company/about_us.html', context)

@login_required(login_url='admin_login')
def company_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Company Dashboard"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)

    # Create an instance of the CompanyForm with the instance set to the logged-in user's company
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Company details updated successfully.')
            return redirect('company_dashboard')

    context = {
        'title': title,
        'form': form,
        'company': company,  # Include the company instance in the context for display
    }

    return render(request, 'company/company_dashboard.html', context)

@login_required(login_url='admin_login')
def business_overview(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Business Overview"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)

    # Retrieve the business_overview object associated with the specified company
    business_overview = CompanyOverview.objects.get(company=company)

    form = CompanyOverviewForm(request.POST or None, request.FILES or None, instance=business_overview)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Business Overview details updated successfully.')
            return redirect('business_overview')

    context = {
        'title': title,
        'form': form,
        'business_overview': business_overview,
    }

    return render(request, 'company/business_overview.html', context)


# @login_required(login_url = 'admin_login')
# def business_overview(request):
#     # Get the Company object with the id equal to 1 from the database
#     company = Company.objects.get(id=1)
#     # print(companies.values)
#     business_overviews = CompanyOverview.objects.filter(id=company.id)
#     # print(business_overviews.values)
#     if request.method == 'POST':
#         form = CompanyOverviewForm(company, request.POST)
#         if form.is_valid():
#             data = CompanyOverview()
#             data.company = form.cleaned_data['company']
#             data.mission = form.cleaned_data['mission']
#             data.vision = form.cleaned_data['vision']
#             data.goal = form.cleaned_data['goal']
#             data.business_overview = form.cleaned_data['business_overview']
#             data.competive_advantage = form.cleaned_data['competive_advantage']
#             data.save()
#             messages.success(request, 'Thank you! Your Business Overview has been created.')
#             return redirect('business_overview')
#     else:
#         form = CompanyOverviewForm(company)

#     context = {
#         'form': form,
#         'business_overviews': business_overviews,
#     }

#     return render(request, 'company/business_overview.html', context)

# @login_required(login_url = 'admin_login')
# def update_business_overview(request, id):
#     # Get the Company object with the id equal to 1 from the database
#     company = Company.objects.get(id=1)
#     business_overviews = CompanyOverview.objects.filter(id=company.id)

#     updated_overview = get_object_or_404(CompanyOverview, company_id=id)
#     form = CompanyOverviewForm(company, request.POST or None, instance=updated_overview)

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('business_overview')

#     context = {
#         'form': form,
#         'business_overviews': business_overviews,
#         'updated_overview': updated_overview,
#     }

#     return render(request, 'company/business_overview.html', context)

# @login_required(login_url = 'admin_login')
# def delete_business_overview(request, id):
#     deleted_overview = CompanyOverview.objects.get(id=id)
#     deleted_overview.delete()
#     return redirect('business_overview')

# @login_required(login_url = 'admin_login')
# def company_dashboard(request):
#     user = Account.objects.get(id=request.user.id)
#     # Get the Company object with the id equal to 1 from the database
#     companies = Company.objects.get(id=1)

#     if request.method == 'POST':
#         form = CompanyForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = Company()
#             data.user = user
#             data.is_client = True
#             data.company_name = form.cleaned_data['company_name']
#             data.website_address = form.cleaned_data['website_address']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.city = form.cleaned_data['city']
#             data.state = form.cleaned_data['state']
#             data.postal_code = form.cleaned_data['postal_code']
#             data.country = form.cleaned_data['country']
#             data.phone = form.cleaned_data['phone']
#             data.logo = form.cleaned_data['logo']
#             data.save()
#             messages.success(request, 'Thank you! Your company has been created.')
#             return redirect('company_dashboard')
#     else:
#         form = CompanyForm()

#     context = {
#         'form': form,
#         'companies': companies
#     }

#     return render(request, 'company/company_dashboard.html', context)

# @login_required(login_url = 'admin_login')
# def update_company(request, id):
#     user = Account.objects.get(id=request.user.id)
#     # Get the Company object with the id equal to 1 from the database
#     company = Company.objects.get(id=1)

#     updated_company = get_object_or_404(Company, id=id)
#     form = CompanyForm(request.POST or None, request.FILES or None, instance=updated_company)

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('company_dashboard')

#     context = {
#         'form': form,
#         'company': company,
#         'updated_company': updated_company,
#     }

#     return render(request, 'company/company_dashboard.html', context)

# @login_required(login_url = 'admin_login')
# def delete_company(request, id):
#     deleted_company = Company.objects.get(id=id, is_client=True)
#     deleted_company.delete()
#     return redirect('company_dashboard')

