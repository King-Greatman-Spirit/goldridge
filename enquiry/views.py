from django.shortcuts import render, redirect
from .models import Lead, Newsletter
from .forms import EnquiryForm, LeadForm
from django.contrib import messages
from company.models import Company
from django.core.mail import EmailMessage
from datetime import datetime
from decouple import config


# Create your views here.
def contact_us(request):
    title = "Contact Us"
    company = Company.objects.all()[0]

    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            data = Lead()
            data.full_name = form.cleaned_data['full_name']
            data.email = form.cleaned_data['email']
            data.company_name = form.cleaned_data['company_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.service = form.cleaned_data['service']
            data.message = form.cleaned_data['message']
            data.channel = form.cleaned_data['channel']
            data.save()

            # USER ACTIVATION EMAIL
            try:
                current_time = datetime.now()
                mail_subject = 'New Contact Alert'
                message = '{} contacted goldridge at {}'.format(
                    form.cleaned_data['full_name'],
                    current_time
                )
                to_email = config('EMAIL_HOST_USER')
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
            except:
                pass

            messages.success(request, 'Thanks for getting in touch with us! Your inquiry has been received')
            return redirect('contact_us')

    else:
        form = EnquiryForm()

    context = {
        'company': company,
        'form': form,
        'title': title,
    }
    return render(request, 'enquiry/contact_us.html', context)

def subscribe(request):

    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            data = Newsletter()
            data.email = form.cleaned_data['email']
            data.save()

            # USER ACTIVATION EMAIL
            try:
                current_time = datetime.now()
                mail_subject = 'Newsletter Subscription Alert'
                message = '{} subscribed with goldridge {}'.format(
                    form.cleaned_data['email'],
                    current_time
                )
                to_email = config('EMAIL_HOST_USER')
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
            except:
                pass

            messages.success(request, "You're officially part of our newsletter community!.")
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))
