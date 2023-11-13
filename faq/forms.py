from django import forms
from .models import FAQCategory, FAQQuestion

class FAQCategoryForm(forms.ModelForm):
    class Meta:
        model = FAQCategory
        fields = ['name', 'home_note']

    # function to loop through form fields and initiat form-control classa
    def __init__(self, *args, **kwargs):
        super(FAQCategoryForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Category Name'
        self.fields['home_note'].widget.attrs['placeholder'] = 'Enter Category Description'

        for field in ('name', 'home_note'):
            self.fields[field].widget.attrs['class'] = 'form-control'

class FAQQuestionForm(forms.ModelForm):
    class Meta:
        model = FAQQuestion
        fields = ['category', 'question', 'answer']

    # function to loop through form fields and initiat form-control class
    def __init__(self, *args, **kwargs):
        super(FAQQuestionForm, self).__init__(*args, **kwargs) # modify what django is giving
        self.fields['category'].empty_label = 'Select Category'
        self.fields['question'].widget.attrs['placeholder'] = 'Enter Question'
        self.fields['answer'].widget.attrs['placeholder'] = 'Enter Answer'

        for field in ('category', 'question', 'answer'):
            self.fields[field].widget.attrs['class'] = 'form-control'



