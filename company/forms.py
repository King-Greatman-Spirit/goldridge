from django import forms
from .models import Company, CompanyOverview

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'website_address', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'phone', 'postal_code', 'country','logo']

    # function to loop through form fields and initiat form-control class
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company_name'].widget.attrs['placeholder'] = 'Enter Company Name'
        self.fields['website_address'].widget.attrs['placeholder'] = 'Enter Website Address'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Address Line 2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter State'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Enter Postal Code'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['logo'].widget.attrs['placeholder'] = 'Upload Logo'

        for field in ('company_name', 'website_address', 'email', 'address_line_1', 'address_line_2', 'city', 'state', 'phone', 'postal_code', 'country','logo'):
            self.fields[field].widget.attrs['class'] = 'form-control'

class CompanyOverviewForm(forms.ModelForm):
    class Meta:
        model = CompanyOverview
        fields = ['company', 'business_overview', 'competive_advantage', 'mission_statement', 'vision', 'philosophy']

    # function to loop through form fields and initiat form-control class
    def __init__(self, companies, *args, **kwargs):
        super(CompanyOverviewForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id__in=companies)
        self.fields['business_overview'].widget.attrs['placeholder'] = 'Enter Company Overview'
        self.fields['competive_advantage'].widget.attrs['placeholder'] = 'Enter Competive Advantage'
        self.fields['mission_statement'].widget.attrs['placeholder'] = 'Enter Mission Statement'
        self.fields['vision'].widget.attrs['placeholder'] = 'Enter Company Vision'
        self.fields['philosophy'].widget.attrs['placeholder'] = 'Enter Company philosophy'

        for field in ('company', 'business_overview', 'competive_advantage', 'mission_statement', 'vision', 'philosophy'):
            self.fields[field].widget.attrs['class'] = 'form-control'

        for field in ('business_overview', 'competive_advantage', 'mission_statement', 'vision', 'philosophy'):
            self.fields[field].widget.attrs['rows'] = 3
