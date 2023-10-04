import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from staff.forms import StaffForm
from accounts.models import Account
from company.models import Company
from staff.models import Staff

from django.utils import timezone
from datetime import datetime

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

    def test_staff_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company': self.test_company.id,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'test@teststaff.com',
            'phone': '11122233344',
            'job_title': 'test job',
            'about': 'my test about',
            'address_line_1': 'address line 1',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'employment_date': datetime(2022, 12, 7, 11, 30, 11, 429000)
        }

        form = StaffForm(self.companies, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)


    def test_staff_form_no_data(self):
        form = StaffForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 13)

