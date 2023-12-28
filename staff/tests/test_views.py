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
        self.login_url = reverse('login')
        self.admin_login_url = reverse('admin_login')
        self.staff_dashboard_url = reverse('staff_dashboard')
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
        self.update_staff_url = reverse('update_staff', args=[self.test_staff.id])
        self.delete_staff_url = reverse('delete_staff', args=[self.test_staff.id])


    def test_staff_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.staff_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'staff/staff_dashboard.html')

    def test_staff_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_staff', self.test_staff.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'staff/staff_dashboard.html')

    def test_update_staff_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
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

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_staff', test_staff.id))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.staff_dashboard_url)
        self.assertFalse(Staff.objects.filter(email='test@teststaff3.com').exists())

    def test_non_admin_user_access(self):
        # Create a client user
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='nonadmin@example.com',
            password='testpass1234',
            username='test first_last'
        )

        # Make the client user as a client, not an admin
        self.user.is_admin = False  # Set 'is_admin' to False to make the user a client
        self.user.is_active = True  # Set 'is_active' to True
        self.user.save()

        # Try to access the staff dashboard as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        response_dashboard = self.client.get(self.staff_dashboard_url)

        # Check that the client is redirected to the login page
        self.assertEquals(response_dashboard.status_code, 302)
        self.assertFalse(response_dashboard.url.startswith(self.staff_dashboard_url))  # Ensure not redirected to staff dashboard

        # Try to access the update staff view as a client
        response_update = self.client.get(self.update_staff_url)

        # Check that the client is redirected to the login page
        self.assertEquals(response_update.status_code, 302)
        self.assertFalse(response_update.url.startswith(self.update_staff_url))  # Ensure not redirected to update staff view

        # Try to access the delete staff view as a client
        response_delete = self.client.get(self.delete_staff_url)

        # Check that the client is redirected to the login page
        self.assertEquals(response_delete.status_code, 302)
        self.assertFalse(response_delete.url.startswith(self.delete_staff_url))  # Ensure not redirected to delete staff view


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