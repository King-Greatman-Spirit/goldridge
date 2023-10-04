from django import forms
from .models import FAQ, FAQCategory
from service.models import Service, ServiceProcess

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['category', 'service', 'service_process', 'question', 'answer']

    def __init__(self, *args, **kwargs):
        super(FAQForm, self).__init__(*args, **kwargs)
        
        # Customize the form fields
        self.fields['category'].empty_label = 'Select Category'
        self.fields['category'].queryset = FAQCategory.objects.all()  # Fetch all FAQ categories
        self.fields['service'].queryset = Service.objects.all()  # Fetch all services
        self.fields['service_process'].queryset = ServiceProcess.objects.all()  # Fetch all service processes
        self.fields['question'].widget.attrs['placeholder'] = 'Enter Question'
        self.fields['answer'].widget.attrs['placeholder'] = 'Enter Answer'  

        for field in ('category', 'service', 'service_process', 'question', 'answer'):
            self.fields[field].widget.attrs['class'] = 'form-control'
