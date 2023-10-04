from django import forms
from .models import Lead, Newsletter

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'full_name',
            'email',
            'phone_number',
            'company_name',
            'no_of_employees',
            'service',
            'message',
            'channel'
         ]
    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        self.fields['service'].empty_label = 'Select Service your interested in'

        self.fields['full_name'].widget.attrs['placeholder'] = 'Enter Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['company_name'].widget.attrs['placeholder'] = 'Enter Company Name'
        self.fields['message'].widget.attrs['placeholder'] = 'Enter Message'

        for field in ('full_name', 'email', 'phone_number', 'company_name'):
            self.fields[field].widget.attrs['class'] = 'gui-input'

        self.fields['message'].widget.attrs['class'] = 'gui-textarea'


class LeadForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            'full_name',
            'email',
            'phone_number'
         ]
    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Enter Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'

        for field in ('full_name', 'email', 'phone_number'):
            self.fields[field].widget.attrs['class'] = 'gui-input'
