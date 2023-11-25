import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Account
from company.models import Company, CompanyOverview
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

img = generate_photo_file()

def url_with_args(name, args):
    return reverse(name, args=[args])

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.staff_dashboard_url = reverse('staff_dashboard')
        self.login_url = reverse('login')
        self.photo_file = ContentFile(img.read(), 'test_image.png')
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
        self.test_company = Company.objects.create(
            id = 1,  # Add this line to set the specific ID for the company
            company_name = 'testcompany',
            website_address = 'http://testcompany.com',
            email = 'test@testcompany.com',
            address_line_1 = 'address line 1',
            city = 'test city',
            state = 'test state',
            postal_code = '111222',
            country = 'test country',
            phone = '11122233344',
            user = self.user,
            logo = self.photo_file
        )
        self.test_staff = Staff.objects.create(
            company         = self.test_company,
            first_name      = 'test first',
            last_name       = 'test last',
            job_title       = 'test job',
            about           = 'my test about',
            phone           =  '11122233344',
            email           = 'test@teststaff.com',
            address_line_1  = 'address line 1',
            city            = 'test city',
            state           = 'test state',
            country         = 'test country',
            # employment_date = datetime(2022, 12, 7, 11, 30, 11, 429000)
            employment_date = timezone.now()
        )


    def test_staff_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.staff_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'staff/staff_dashboard.html')

    def test_staff_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        photo_file = generate_photo_file()

        res = self.client.post(self.staff_dashboard_url, {
           'company': self.test_company.id,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'test@teststaff2.com',
            'phone': '11122233344',
            'photo': photo_file,
            'job_title': 'test job',
            'about': 'my test about',
            'address_line_1': 'address line 1',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'employment_date': datetime(2022, 12, 7, 11, 30, 11, 429000)
        }, format='multipart')
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.assertTrue(Company.objects.filter(email='test@testcompany.com').exists())
        self.assertRedirects(res, self.staff_dashboard_url)

    def test_update_staff_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_staff', self.test_staff.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'staff/staff_dashboard.html')

    def test_update_staff_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload = {
            'company': self.test_company.id,
            'first_name': 'first',
            'last_name': 'last',
            'email': 'test@teststaff.com',
            'phone': '11122233344',
            'photo': photo_file,
            'job_title': 'test job',
            'about': 'my test about',
            'address_line_1': 'address line 1',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'employment_date': datetime(2022, 12, 7, 11, 30, 11, 429000)
            # 'employment_date' : timezone.now()
        }

        res = self.client.post(
            url_with_args('update_staff', self.test_staff.id),
            payload,
            format='multipart'
        )
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.test_staff.refresh_from_db()
        self.assertEqual(str(self.test_staff), payload['first_name'])
        self.assertRedirects(res, self.staff_dashboard_url)

    def test_delete_staff(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        test_staff = Staff.objects.create(
            company         = self.test_company,
            first_name      = 'test first',
            last_name       = 'test last',
            job_title       = 'test job',
            about           = 'my test about',
            phone           =  '11122233344',
            email           = 'test@teststaff3.com',
            address_line_1  = 'address line 1',
            city            = 'test city',
            state           = 'test state',
            country         = 'test country',
            # employment_date = datetime(2022, 12, 7, 11, 30, 11, 429000)
            employment_date = timezone.now()
        )

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_staff', test_staff.id))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.staff_dashboard_url)
        self.assertFalse(Staff.objects.filter(email='test@teststaff3.com').exists())

def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/staff')
    files = [i for i in os.listdir(images_path)
            if os.path.isfile(os.path.join(images_path, i))
            and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))

    logos_images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    logos_files = [i for i in os.listdir(logos_images_path)
             if os.path.isfile(os.path.join(logos_images_path, i))
             and i.startswith('test_')]

    for file in logos_files:
        os.remove(os.path.join(logos_images_path, file))