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
from service.models import Service, ServiceProcess
from staff.models import Staff

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file

def url_with_args(name, args):
    return reverse(name, args=[args])

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.company_url = reverse('company')
        self.company_dashboard_url = reverse('company_dashboard')
        self.BO_url = reverse('business_overview')
        self.login_url = reverse('login')
        self.photo_file = generate_photo_file()
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
            user = self.user,
            logo = ContentFile(self.photo_file.read(), 'test_image.png')
        )
        self.test_company_overview = CompanyOverview.objects.create(
            company = self.test_company,
            business_overview = 'test business overview',
            competive_advantage = 'test competitive advantage',
            mission = 'test mission statement',
            vision = 'test vision',
            goal = 'test philosophy'
        )


    def test_company(self):
        res = self.client.get(self.company_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/about_us.html')

    def test_company_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.company_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/company_dashboard.html')

    def test_company_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        res = self.client.post(self.company_dashboard_url, {
            'company_name': 'testcompany2',
            'website_address': 'http://testcompany2.com',
            'email': 'test@testcompany2.com',
            'address_line_1': 'address line 1',
            'address_line_2': 'address line 2',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'phone': '11122233344',
            'logo': photo_file,
        }, format='multipart')
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.assertTrue(Company.objects.filter(email='test@testcompany2.com').exists())
        self.assertRedirects(res, self.company_dashboard_url)

    def test_update_company_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_company', self.test_company.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/company_dashboard.html')

    def test_update_company_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload = {
            'company_name': 'test company2',
            'website_address': 'http://testcompany2.com',
            'email': 'test2@testcompany2.com',
            'address_line_1': 'address line 1',
            'address_line_2': 'address line 2',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111232',
            'country': 'test country',
            'phone': '11122233344',
            'logo': photo_file,
        }

        res = self.client.post(
            url_with_args('update_company', self.test_company.id),
            payload,
            format='multipart'
        )
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.test_company.refresh_from_db()
        self.assertEqual(str(self.test_company), payload['company_name'])
        self.assertRedirects(res, self.company_dashboard_url)

    def test_delete_company(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        test_firm = Company.objects.create(
            company_name = 'testcompany3',
            website_address = 'http://testcompany3.com',
            email = 'test@testcompany3.com',
            address_line_1 = 'address line 1',
            city = 'test city',
            state = 'test state',
            postal_code = '111222',
            country = 'test country',
            phone = '11122233344',
            is_client = True,
            user = self.user
        )

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_company', test_firm.id))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.company_dashboard_url)
        self.assertFalse(Company.objects.filter(email='test@testcompany3.com').exists())

    def test_BO_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.BO_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/business_overview.html')

    def test_BO_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        company_res = self.client.post(self.company_dashboard_url, {
            'company_name': 'testcompany2',
            'website_address': 'http://testcompany2.com',
            'email': 'test@testcompany2.com',
            'address_line_1': 'address line 1',
            'address_line_2': 'address line 2',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'phone': '11122233344',
            'logo': photo_file,
        }, format='multipart')
        company = Company.objects.get(email='test@testcompany2.com')

        BO_res = self.client.post(self.BO_url,{
            'company': company.id,
            'business_overview': 'test business overview',
            'competive_advantage': 'test competitive advantage',
            'mission': 'test mission statement',
            'vision': 'test vision',
            'goal': 'test philosophy'
        })

        self.assertEquals(BO_res.status_code, 302)
        self.assertTrue(CompanyOverview.objects.filter(company_id=company.id).exists())
        self.assertRedirects(BO_res, self.BO_url)

    def test_update_BO_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_business_overview', self.test_company.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/business_overview.html')

    def test_update_BO_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload = {
            'company': self.test_company.id,
            'business_overview': 'test overview',
            'competive_advantage': 'test advantage',
            'mission': 'test mission statement',
            'vision': 'test vision',
            'goal': 'test philosophy'
        }

        res = self.client.post(
            url_with_args('update_business_overview', self.test_company.id),
            payload
        )
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.test_company_overview.refresh_from_db()
        BO = CompanyOverview.objects.get(company_id=self.test_company.id)
        for k, v in payload.items():
            if k != 'company':
                # print(getattr(BO, k), k, v)
                self.assertEqual(getattr(BO, k), v)
        self.assertRedirects(res, self.BO_url)

    def test_delete_BO(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args(
            'delete_business_overview',
            self.test_company_overview.id
        ))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.BO_url)
        self.assertFalse(
            CompanyOverview.objects.filter(id=self.test_company_overview.id).exists()
        )


def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))
