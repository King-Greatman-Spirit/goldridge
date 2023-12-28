from django import forms
from .models import Service, ServiceProcess, SubService, SubServiceType, approval_chioce
from company.models import Company
from shortuuid import ShortUUID  # Add this import statement
from shortuuid.django_fields import ShortUUIDField


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
        fields = ['company', 'service', 'subServiceType', 'description', 'duration', 'rate', 'target', 'approval', 'approval_note', 'char_id']

    def __init__(self, company, *args, **kwargs):
        super(SubServiceForm, self).__init__(*args, **kwargs)

        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['service'].empty_label = 'Select Service'
        self.fields['subServiceType'].empty_label = 'Select Service Application Type'

        self.fields['description'].widget.attrs['placeholder'] = 'Describe Service Application'
        self.fields['description'].widget.attrs['rows'] = 3

        self.fields['approval'].widget = forms.Select(choices=approval_chioce, attrs={'class': 'form-control'})
        self.fields['approval'].required = False
        self.fields['approval_note'].required = False
        self.fields['duration'].widget.attrs['placeholder'] = 'Enter Duration'
        self.fields['rate'].widget.attrs['placeholder'] = 'Enter Rate'
        self.fields['target'].widget.attrs['placeholder'] = 'Enter Amount'

        # Make char_id read-only in the form
        self.fields['char_id'].widget.attrs['readonly'] = True
        self.fields['char_id'].required = False

        for field in ('company', 'service', 'subServiceType', 'description', 'duration', 'rate', 'target', 'approval', 'approval_note', 'char_id'):
            self.fields[field].widget.attrs['class'] = 'form-control'

class SubServiceTypeForm(forms.ModelForm):
    class Meta:
        model = SubServiceType
        fields = ['company', 'service', 'type', 'abbr', 'description']

    # function to loop through form fields and initiat form-control class
    def __init__(self, company, *args, **kwargs):
        super(SubServiceTypeForm, self).__init__(*args, **kwargs)
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)

        self.fields['service'].empty_label = 'Select Service'

        self.fields['type'].widget.attrs['placeholder'] = 'Enter SubService Type'
        self.fields['abbr'].widget.attrs['placeholder'] = 'Enter Abbreviation'

        self.fields['description'].widget.attrs['placeholder'] = 'Describe SubService Type'
        self.fields['description'].widget.attrs['rows'] = 3

        for field in ('company', 'service', 'type', 'abbr', 'description'):
            self.fields[field].widget.attrs['class'] = 'form-control'