from django import forms
from .models import Service, ServiceProcess, SubService, SubServiceType, approval_chioce
from company.models import Company


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['company', 'service_name', 'slug', 'service_description', 'image']

    # function to loop through form fields and initiat form-control class
    def __init__(self, company, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)

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
    def __init__(self, company, *args, **kwargs):
        super(ServiceProcessForm, self).__init__(*args, **kwargs)
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)

        self.fields['service'].empty_label = 'Select Service'

        self.fields['process_name'].widget.attrs['placeholder'] = 'Enter Process Name'

        self.fields['process_description'].widget.attrs['placeholder'] = 'Describe Process'
        self.fields['process_description'].widget.attrs['rows'] = 3

        self.fields['image'].widget.attrs['placeholder'] = 'Upload Image'

        for field in ('company', 'service', 'process_name', 'process_description', 'image'):
            self.fields[field].widget.attrs['class'] = 'form-control'

class SubServiceForm(forms.ModelForm):
    class Meta:
        model = SubService
        fields = ['company', 'service', 'subServiceType', 'description', 'duration', 'rate', 'target', 'approval', 'approval_note']

    # function to loop through form fields and initiat form-control class
    def __init__(self, company, *args, **kwargs):
        super(SubServiceForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)

        self.fields['service'].empty_label = 'Select Service'

        self.fields['subServiceType'].empty_label = 'Select Service Application Type'

        self.fields['description'].widget.attrs['placeholder'] = 'Describe Service Application'
        self.fields['description'].widget.attrs['rows'] = 3
        
        # Render the approval field manually to apply the custom class
        self.fields['approval'].widget = forms.Select(choices=approval_chioce, attrs={'class': 'form-control'})
        # Mark approval and approval_note as not required
        self.fields['approval'].required = False
        self.fields['approval_note'].required = False
        self.fields['duration'].widget.attrs['placeholder'] = 'Enter Duration'
        self.fields['rate'].widget.attrs['placeholder'] = 'Enter Rate'
        self.fields['target'].widget.attrs['placeholder'] = 'Enter Amount'

        for field in ('company', 'service', 'subServiceType', 'description', 'duration', 'rate', 'target', 'approval_note'):
            self.fields[field].widget.attrs['class'] = 'form-control'

            