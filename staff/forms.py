from django import forms
from .models import Staff
from company.models import Company

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['company', 'first_name', 'last_name', 'email', 'phone', 'job_title', 'about', 'photo', 'address_line_1', 'address_line_2', 'city', 'state', 'country','employment_date', 'is_management', 'is_primary_contact']

    # function to loop through form fields and initiat form-control class
    def __init__(self, companies, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id__in=companies)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['job_title'].widget.attrs['placeholder'] = 'Enter Job Title'
        self.fields['about'].widget.attrs['placeholder'] = 'Describe Job Title'
        self.fields['about'].widget.attrs['rows'] = 3
        self.fields['photo'].widget.attrs['placeholder'] = 'Upload Photo'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Address Line 2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter State'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'

        self.fields['employment_date'].input_formats = '%d-%m-%Y %H:%M:%S'
        self.fields['employment_date'].widget.attrs['class'] = 'form-control datetimepicker'

        self.fields['is_management'].widget.attrs['placeholder'] = 'Management'
        self.fields['is_primary_contact'].widget.attrs['placeholder'] = 'Primary Contact'

        for field in ('company', 'first_name', 'last_name', 'email', 'phone', 'job_title', 'about', 'photo', 'address_line_1', 'address_line_2', 'city', 'state', 'country'):
            self.fields[field].widget.attrs['class'] = 'form-control'

        for field in ('is_management', 'is_primary_contact'):
            self.fields[field].widget.attrs['class'] = 'form-check-input'
