from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Service, ServiceProcess, Testimonial,
    SubServiceType, SubService, Prerequisite, Transaction
)
from company.models import Company
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .forms import ServiceForm, ServiceProcessForm, SubServiceForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q


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
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Service Dashboard"
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
        'title': title,
        'form': form,
        'services': services,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
     
    title = "Update Services"
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    # Retrieve all Service objects associated with the specified company (e.g., Goldridge) from the database
    services = Service.objects.filter(company=company)

    updated_service = get_object_or_404(Service, id=id)
    form = ServiceForm(company, request.POST or None, request.FILES or None, instance=updated_service)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Services updated successfully.')
            return redirect('service_dashboard')

    context = {
        'title': title,
        'form': form,
        'services': services,
        'updated_service': updated_service,
    }

    return render(request, 'service/service_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_service = Service.objects.get(id=id)
    deleted_service.delete()
    return redirect('service_dashboard')

@login_required(login_url = 'admin_login')
def service_process_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Service Processes"
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
        'title': title,
        'form': form,
        'service_processes': service_processes,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def update_service_process(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Update Service Processes"
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
            messages.success(request, 'Service Processes updated successfully.')
            return redirect('service_process_dashboard')

    context = {
        'title': title,
        'form': form,
        'service_processes': service_processes,
        'updated_sp': updated_sp,
    }

    return render(request, 'service/service_process_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_service_process(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_service_processes = ServiceProcess.objects.get(id=id)
    deleted_service_processes.delete()
    return redirect('service_process_dashboard')

@login_required(login_url='login')
def user_subService_dashboard(request):
    title = "User Service Applications"
    user = get_object_or_404(Account, id=request.user.id)  # Ensure user exists
    company = Company.objects.get(id=1)

    # Retrieve only the user's service applications
    subservices = SubService.objects.filter(user=user)

    if request.method == 'POST':
        form = SubServiceForm(company, request.POST)
        if form.is_valid():
            data = SubService()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.subServiceType = form.cleaned_data['subServiceType']
            data.user = user  # Assign the user obtained from the request to the 'user' field
            data.description = form.cleaned_data['description']
            # Handle approval and approval_note separately
            if 'approval' in form.cleaned_data:
                data.approval = form.cleaned_data['approval']
            if 'approval_note' in form.cleaned_data:
                data.approval_note = form.cleaned_data['approval_note']
            data.duration = form.cleaned_data['duration']
            data.rate = form.cleaned_data['rate']
            data.target = form.cleaned_data['target']
            # Set the user field in the form before saving
            form.instance.user = user
            data.save()
            messages.success(request, 'Thank you! Your Service Application has been created.')
            return redirect('user_service_applications')  # Update this line
        # else:
        #     print(form.errors)  # Add this line for debugging
        #     messages.error(request, 'Form submission failed. Please check the form for errors.')

    else:
        form = SubServiceForm(company)

    context = {
        'title': title,
        'form': form,
        'subservices': subservices,
    }

    return render(request, 'service/user_subService_dashboard.html', context)

@login_required(login_url='admin_login')
def admin_subService_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    # Update existing records with a default value for 'approval'
    SubService.objects.filter(approval='').update(approval='Pending')
    
    title = "Admin Service Applications"
    user = Account.objects.get(id=request.user.id)
    company = Company.objects.get(id=1)
    
    # Retrieve and order user service applications by 'approval' (descending) and 'created_date' (ascending).
    user_service_applications = SubService.objects.all().order_by('-approval', 'created_date')

    if request.method == 'POST':
        form = SubServiceForm(company, request.POST)
        if form.is_valid():
            return redirect('admin_service_applications')  # Update this line

    else:
        form = SubServiceForm(company)

    context = {
        'form': form,
        'title': title,
        'user_service_applications': user_service_applications,
    }

    return render(request, 'service/admin_subService_dashboard.html', context)

@login_required(login_url='admin_login')
def update_admin_subService(request, id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to update this service application.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    # Update existing records with a default value for 'approval'
    SubService.objects.filter(approval='').update(approval='Pending')
    
    title = "Update Service Applications"
    user = Account.objects.get(id=request.user.id)
    company = Company.objects.get(id=1)

    # Retrieve and order user service applications by 'approval' (descending) and 'created_date' (ascending).
    user_service_applications = SubService.objects.all().order_by('-approval', 'created_date')


    # Get the specific service record
    updated_asa = get_object_or_404(user_service_applications, id=id)
    form = SubServiceForm(company, request.POST or None, instance=updated_asa)

    if request.method == 'POST':
        if form.is_valid():
            data = SubService()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.subServiceType = form.cleaned_data['subServiceType']
            data.user = user  # Assign the user obtained from the request to the 'user' field
            data.description = form.cleaned_data['description']
            # Make approval and approval_note compulsory
            data.approval = form.cleaned_data['approval']
            data.approval_note = form.cleaned_data['approval_note']
            data.duration = form.cleaned_data['duration']
            data.rate = form.cleaned_data['rate']
            data.target = form.cleaned_data['target']
            form.save()
            messages.success(request, 'Service Application updated successfully.')
            return redirect('admin_service_applications')  # Redirect to the appropriate page after updating

    context = {
        'form': form,
        'title': title,
        'user_service_applications': user_service_applications,
        'updated_asa': updated_asa,  # Pass the instance to prepopulate the form
    }

    return render(request, 'service/admin_subService_dashboard.html', context)


@login_required(login_url = 'admin_login')
def delete_admin_subService(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_admin_subService = SubService.objects.get(id=id)
    deleted_admin_subService.delete()
    return redirect('admin_service_applications')

@login_required(login_url = 'admin_login')
def apps_by_type(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    title = "Application By Type"
    # user = Account.objects.get(id=request.user.id)
    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)
    services = Service.objects.filter(company=company)

    context = {
        'title': title,
        'services': services,
    }

    return render(request, 'service/app_by_type/app_by_type.html', context)


# Ensure that only admin users can access the type_dashboard view
@login_required(login_url='admin_login')
def type_dashboard(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        # If not an admin, display an error message and redirect to the login page
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users

    # Update existing records with a default value for 'approval'
    SubService.objects.filter(approval='').update(approval='Pending')

    # Get the current user and company information
    user = Account.objects.get(id=request.user.id)
    company = Company.objects.get(id=1)
    
    # Get the specific service based on the provided ID
    service = get_object_or_404(Service, id=id)

    # Set the title for the type_dashboard page
    title = f"Apps Type: {service.service_name}"

    # Retrieve and order apps type by 'approval' (descending) and 'created_date' (ascending).
    apps_type = SubService.objects.filter(company=company, service=service).order_by('-approval', 'created_date')

    # Print the content of apps_type for debugging
    # print(apps_type.values())

    # Check if the form is submitted via POST request
    if request.method == 'POST':

        # Initialize a SubServiceForm with company and POST data
        form = SubServiceForm(company, request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Redirect to the same type_dashboard view with the specific service ID
            return redirect('type-dashboard', id=id)
    else:
        # Move the form initialization outside of the if block
        form = SubServiceForm(company)

    # Prepare the context to be passed to the template
    context = {
        'title': title,
        'apps_type': apps_type,
        'form': form,
        'service': service,
    }

    # Render the type_dashboard.html template with the provided context
    return render(request, 'service/app_by_type/type_dashboard.html', context)


@login_required(login_url='admin_login')
def update_type_dashboard(request, service_id, app_id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to update this service application.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    # Update existing records with a default value for 'approval'
    SubService.objects.filter(approval='').update(approval='Pending')
    
    # Get the current user and company information
    user = Account.objects.get(id=request.user.id)
    company = Company.objects.get(id=1)
    
    # Get the specific service based on the provided service ID
    service = get_object_or_404(Service, id=service_id)

    # Set the title for the type_dashboard page
    title = f"Update Apps Type: {service.service_name}"

    # Retrieve and order apps type by 'approval' (descending) and 'created_date' (ascending).
    apps_type = SubService.objects.filter(company=company, service=service).order_by('-approval', 'created_date')

    # Get the specific service application based on the provided ID
    updated_td = get_object_or_404(apps_type, id=app_id)
    form = SubServiceForm(company, request.POST or None, instance=updated_td)

    if request.method == 'POST':
        # print(request.path)
        if form.is_valid():
            data = SubService()
            data.company = form.cleaned_data['company']
            data.service = form.cleaned_data['service']
            data.subServiceType = form.cleaned_data['subServiceType']
            data.user = user  # Assign the user obtained from the request to the 'user' field
            data.description = form.cleaned_data['description']
            # Make approval and approval_note compulsory
            data.approval = form.cleaned_data['approval']
            data.approval_note = form.cleaned_data['approval_note']
            data.duration = form.cleaned_data['duration']
            data.rate = form.cleaned_data['rate']
            data.target = form.cleaned_data['target']
            form.save()
            messages.success(request, 'Dashboard updated successfully.')
            # Redirect to the 'type-dashboard' page for the specific service ID after updating.
            # Redirect to the 'type-dashboard' page for the specific service ID after updating.
            return redirect('type-dashboard', id=service.id)


    context = {
        'form': form,
        'title': title,
        'apps_type': apps_type,
        'service': service,
        'updated_td': updated_td,  # Pass the instance to prepopulate the form
    }

    return render(request, 'service/app_by_type/type_dashboard.html', context)

@login_required(login_url = 'admin_login')
def delete_type_dashboard(request, id):
    # Ensure the user is an admin
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')  # Redirect to a suitable page for non-admin users
    
    deleted_type_dashboard = SubService.objects.get(id=id)
    deleted_type_dashboard.delete()
    return redirect('type-dashboard', id=deleted_type_dashboard.service.id)

@login_required(login_url='admin_login')
def clients_table(request):
    # Ensure the user is an admin
    if not request.user.is_admin:
        # Redirect non-admin users to the login page with an error message
        messages.error(request, 'You do not have permission to access the admin dashboard.')
        return redirect('login')

    # Set the title for the page
    title = "Clients Table"

    # Get the Company object with the id equal to 1 from the database
    company = Company.objects.get(id=1)

    # Fetch all users excluding admin and super admin
    users = Account.objects.filter(~Q(is_admin=True) & ~Q(is_superadmin=True))

    # Collect user data for the table
    users_data = []
    for user in users:
        # Get subservice abbreviations for the user
        subservice_abbr = get_user_subservice_abbr(user)
        
        # Append user data to the list
        users_data.append({
            'name': f'{user.first_name} {user.last_name}',
            'email': user.email,
            'phone_number': user.phone_number,
            'subservice_abbr': subservice_abbr,
        })

    # Prepare the context to be passed to the template
    context = {
        'title': title,
        'company': company,
        'users_data': users_data,
    }

    # Render the template with the provided context
    return render(request, 'accounts/admin/clients_table.html', context)

# Helper function to get distinct subservice abbreviations for a user
def get_user_subservice_abbr(user):
    # Query SubService objects related to the user
    subservices = SubService.objects.filter(user=user)

    # Extract distinct SubServiceType abbreviations using set()
    subservice_abbr_set = set(subservice.subServiceType.abbr for subservice in subservices)

    # Join the set of abbreviations into a string, or return 'None' if the set is empty
    return ', '.join(subservice_abbr_set) if subservice_abbr_set else 'None'

