from django.test import TestCase
from faq.models import FAQCategory
from faq.forms import FAQForm

class TestFAQForm(TestCase):

    def setUp(self):
        # Create a sample FAQCategory instance for testing
        self.category = FAQCategory.objects.create(name='Sample Category')

    def test_faq_form_valid_data(self):
        data = {
            'category': self.category.id,
            'question': 'Sample Question',
            'answer': 'Sample Answer'
        }

        form = FAQForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_faq_form_no_data(self):
        form = FAQForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)  # Three fields are required: category, question, and answer
