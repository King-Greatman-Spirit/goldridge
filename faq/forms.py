from django import forms
from .models import FAQCategory, FAQQuestion

class FAQCategoryForm(forms.ModelForm):
    class Meta:
        model = FAQCategory
        fields = ['name']

    # function to loop through form fields and initiat form-control classa
    def __init__(self, *args, **kwargs):
        super(FAQCategoryForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Category Name'

        # self.fields['name'].widget.attrs['class'] = 'textareagui-textarea'
        self.fields['name'].widget.attrs['class'] = 'form-control'




