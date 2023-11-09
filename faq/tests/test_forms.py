import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from faq.forms import FAQCategoryForm
from accounts.models import Account
from company.models import Company, CompanyOverview
from faq.models import FAQCategory, FAQQuestion

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file


class TestForms(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
        self.test_company = Company.objects.create(
            company_name = 'testcompany',
            website_address = 'http://testcompany.com',
            email = 'test@testcompany.com',
            address_line_1 = 'address line 1',
            city = 'test city',
            state = 'test state',
            postal_code = '111222',
            country = 'test country',
            phone = '11122233344',
            user = self.user
        )
        self.companies = Company.objects.filter(user=self.user)
        self.test_FAQCategory = FAQCategory.objects.create(
            home_note   = 'test home note',
            name = 'test name'
        )

        # Create a FAQ in the test category
        self.test_FAQQuestion = FAQQuestion.objects.create(
            category=self.test_FAQCategory,
            question='Test Question',
            answer='Test Answer',
        )

    def test_faq_category_form_valid_data(self):

        data = {
            'name': 'test category'
        }

        form = FAQCategoryForm(data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_faq_category_form_no_data(self):
        form = FAQCategoryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
