import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from company.forms import CompanyForm, CompanyOverviewForm
from accounts.models import Account
from company.models import Company, CompanyOverview

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

    def test_company_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'logo': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company_name': 'testcompany2',
            'website_address': 'http://testcompany2.com',
            'email': 'test@testcompany2.com',
            'address_line_1': 'address line 1',
            'address_line_2': 'address line 2',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'phone': '11122233344'
        }

        form = CompanyForm(data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_company_form_no_data(self):
        form = CompanyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 10)

    def test_BO_form_valid_data(self):

        data = {
            'company': self.test_company.id,
            'business_overview': 'test overview',
            'competive_advantage': 'test advantage',
            'mission': 'test mission',
            'vision': 'test vision',
            'goal': 'test philosophy'
        }

        form = CompanyOverviewForm(self.companies, data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_BO_form_no_data(self):
        form = CompanyOverviewForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)