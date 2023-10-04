from django import forms
from .models import Service, ServiceProcess
from company.models import Company

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['company', 'service_name', 'slug', 'service_description', 'image']

    # function to loop through form fields and initiat form-control class
    def __init__(self, companies, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id__in=companies)

        self.fields['service_name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['service_name'].widget.attrs['class'] = 'service form-control'

        self.fields['slug'].widget.attrs['readonly'] = 'readonly'
        self.fields['slug'].widget.attrs['class'] = 'slug form-control'

        self.fields['service_description'].widget.attrs['placeholder'] = 'Describe Service'
        self.fields['service_description'].widget.attrs['rows'] = 3

        self.fields['image'].widget.attrs['placeholder'] = 'Upload Image'

        for field in ('company', 'service_description', 'image'):
            self.fields[field].widget.attrs['class'] = 'form-control'

class ServiceProcessForm(forms.ModelForm):
    class Meta:
        model = ServiceProcess
        fields = ['company', 'service', 'process_name', 'process_description', 'image']

    # function to loop through form fields and initiat form-control class
    def __init__(self, companies, *args, **kwargs):
        super(ServiceProcessForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id__in=companies)

        self.fields['service'].empty_label = 'Select Service'

        self.fields['process_name'].widget.attrs['placeholder'] = 'Enter Process Name'

        self.fields['process_description'].widget.attrs['placeholder'] = 'Describe Process'
        self.fields['process_description'].widget.attrs['rows'] = 3

        self.fields['image'].widget.attrs['placeholder'] = 'Upload Image'

        for field in ('company', 'service', 'process_name', 'process_description', 'image'):
            self.fields[field].widget.attrs['class'] = 'form-control'
