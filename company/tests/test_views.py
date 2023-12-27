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
        self.admin_login_url = reverse('admin_login')
        self.photo_file = generate_photo_file()
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
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.company_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/company_dashboard.html')

    def test_company_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

         # Simulate a POST request to update company details
        photo_file = generate_photo_file()
        res = self.client.post(self.company_dashboard_url, {
            'company_name': 'testcompany2',
            'website_address': 'http://testcompany2.com',
            'email': 'test@testcompany.com',
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

        # Check the response status code
        self.assertEquals(res.status_code, 302)

        # Retrieve the updated Company instance
        updated_company = Company.objects.get(email='test@testcompany.com')

        # Check whether the Company details are updated successfully
        self.assertEquals(updated_company.company_name, 'testcompany2')
        self.assertEquals(updated_company.website_address, 'http://testcompany2.com')

        # Check the redirection
        self.assertRedirects(res, self.company_dashboard_url)

    def test_BO_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        res = self.client.get(self.BO_url)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/business_overview.html')

    def test_BO_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        # Ensure the admin user is logged in
        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        # Make a POST request to update company information
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

        # Make a POST request to update business overview
        BO_res = self.client.post(self.BO_url,{
            'company': company.id,
            'business_overview': 'test business overview',
            'competive_advantage': 'test competitive advantage',
            'mission': 'test mission statement',
            'vision': 'test vision',
            'goal': 'test philosophy'
        })

        # Check the status codes and template usage
        self.assertEquals(company_res.status_code, 302)
        self.assertEquals(BO_res.status_code, 302)

        # Check if the data is updated in the database
        updated_company_overview = CompanyOverview.objects.get(company=company)
        self.assertEquals(updated_company_overview.goal, 'test philosophy')

        # Check the redirection
        self.assertRedirects(BO_res, self.BO_url)

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

        # Try to access the company dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.company_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the company dashboard
        self.assertEquals(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.company_dashboard_url))  # Ensure not redirected to company dashboard view

        # Try to access the business operations view as a client
        res_bo = self.client.get(self.BO_url)

        # Check that the client is redirected to the login page when attempting to access business operations view
        self.assertEquals(res_bo.status_code, 302)
        self.assertFalse(res_bo.url.startswith(self.BO_url))  # Ensure not redirected to business operations view



    # def test_update_company_GET(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })

    #     res = self.client.get(url_with_args('update_company', self.test_company.id))

    #     self.assertEquals(res.status_code, 200)
    #     self.assertTemplateUsed(res, 'company/company_dashboard.html')

    # def test_update_company_POST(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })

    #     photo_file = generate_photo_file()

    #     payload = {
    #         'company_name': 'test company2',
    #         'website_address': 'http://testcompany2.com',
    #         'email': 'test@testcompany.com',
    #         'address_line_1': 'address line 1',
    #         'address_line_2': 'address line 2',
    #         'city': 'test city',
    #         'state': 'test state',
    #         'postal_code': '111232',
    #         'country': 'test country',
    #         'phone': '11122233344',
    #         'logo': photo_file,
    #     }

    #     res = self.client.post(
    #         url_with_args('update_company', self.test_company.id),
    #         payload,
    #         format='multipart'
    #     )
    #     # print(res.context['form'].errors)

    #     self.assertEquals(res.status_code, 302)
    #     self.test_company.refresh_from_db()
    #     self.assertEqual(str(self.test_company), payload['company_name'])
    #     self.assertRedirects(res, self.company_dashboard_url)

    # def test_delete_company(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     test_firm = Company.objects.create(
    #         company_name = 'testcompany3',
    #         website_address = 'http://testcompany3.com',
    #         email = 'test@testcompany3.com',
    #         address_line_1 = 'address line 1',
    #         city = 'test city',
    #         state = 'test state',
    #         postal_code = '111222',
    #         country = 'test country',
    #         phone = '11122233344',
    #         is_client = True,
    #         user = self.user
    #     )

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })

    #     res = self.client.get(url_with_args('delete_company', test_firm.id))

    #     self.assertEquals(res.status_code, 302)
    #     self.assertRedirects(res, self.company_dashboard_url)
    #     self.assertFalse(Company.objects.filter(email='test@testcompany3.com').exists())

    # def test_update_BO_GET(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })

    #     res = self.client.get(url_with_args('update_business_overview', self.test_company.id))

    #     self.assertEquals(res.status_code, 200)
    #     self.assertTemplateUsed(res, 'company/business_overview.html')

    # def test_update_BO_POST(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })
    #     payload = {
    #         'company': self.test_company.id,
    #         'business_overview': 'test overview',
    #         'competive_advantage': 'test advantage',
    #         'mission': 'test mission statement',
    #         'vision': 'test vision',
    #         'goal': 'test philosophy'
    #     }

    #     res = self.client.post(
    #         url_with_args('update_business_overview', self.test_company.id),
    #         payload
    #     )
    #     # print(res.context['form'].errors)

    #     self.assertEquals(res.status_code, 302)
    #     self.test_company_overview.refresh_from_db()
    #     BO = CompanyOverview.objects.get(company_id=self.test_company.id)
    #     for k, v in payload.items():
    #         if k != 'company':
    #             # print(getattr(BO, k), k, v)
    #             self.assertEqual(getattr(BO, k), v)
    #     self.assertRedirects(res, self.BO_url)

    # def test_delete_BO(self):
    #     test_user = Account.objects.get(email='user1@example.com')
    #     test_user.is_active = True
    #     test_user.save()

    #     admin_login_res = self.client.post(self.admin_login_url, {
    #         'email' : 'user1@example.com',
    #         'password': 'testpass1234'
    #     })

    #     res = self.client.get(url_with_args(
    #         'delete_business_overview',
    #         self.test_company_overview.id
    #     ))

    #     self.assertEquals(res.status_code, 302)
    #     self.assertRedirects(res, self.BO_url)
    #     self.assertFalse(
    #         CompanyOverview.objects.filter(id=self.test_company_overview.id).exists()
    #     )


def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))
