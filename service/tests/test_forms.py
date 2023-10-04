import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from accounts.models import Account
from company.models import Company
from service.models import Service, ServiceProcess
from service.forms import ServiceForm, ServiceProcessForm

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
        self.test_service = Service.objects.create(
            company             = self.test_company,
            service_name        = 'test service',
            slug                = 'test_service',
            service_description =  'my test service'
        )
        self.companies = Company.objects.filter(user=self.user)

    def test_service_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'               : self.test_company.id,
            'service_name'          : 'test service two',
            'slug'                  : 'test_service_two',
            'service_description'   : 'my test service'
        }

        form = ServiceForm(self.companies, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_service_form_no_data(self):
        form = ServiceForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_service_process_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'process_name'          : 'test process name',
            'process_description'   : 'test process description'
        }

        form = ServiceProcessForm(self.companies, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_service_process_form_no_data(self):
        form = ServiceProcessForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

