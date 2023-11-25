import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Account
from company.models import Company
from service.models import (
    Service, ServiceProcess, Testimonial, SubServiceType, 
    SubService, Prerequisite, Transaction, approval_chioce
)

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
        self.service_dashboard_url = reverse('service_dashboard')
        self.SPD_url = reverse('service_process_dashboard')
        self.company_dashboard_url = reverse('company_dashboard')
        self.login_url = reverse('login')
        self.USD_url = reverse('user_subService_dashboard')
        self.setUp_file = generate_photo_file()
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
            logo = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_service = Service.objects.create(
            company             = self.test_company,
            service_name        = 'test service',
            slug                = 'test_service',
            service_description = 'Testing service description',
            image               = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_service_process = ServiceProcess.objects.create(
            company             = self.test_company,
            service             = self.test_service,
            process_name        = 'test process',
            process_description = 'my test process',
            image               = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_subservice_type = SubServiceType.objects.create(
            company               = self.test_company,
            service               = self.test_service,
            type                  = 'test type',
            description           = 'test description'
        )
        self.test_user_subservice    = SubService.objects.create(
            company                  = self.test_company,
            service                  = self.test_service,
            subServiceType           = self.test_subservice_type,
            user                     = self.user,
            description              = 'test description',
            approval                 = approval_chioce[3][0],
            duration                 = 6,
            rate                     = 3,
            target                   = 5000
        )


    def test_service(self):
        res = self.client.get(url_with_args('service_slug',  self.test_service.slug))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service.html')


    def test_service_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.service_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_service_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        res = self.client.post(self.service_dashboard_url, {
            'company'               : self.test_company.id,
            'service_name'          : 'test service two',
            'slug'                  : 'test_service_two',
            'service_description'   : 'my test service',
            'image'                 : photo_file,
        }, format='multipart')
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.assertTrue(Company.objects.filter(email='test@testcompany.com').exists())
        self.assertTrue(Service.objects.filter(service_name='test service two').exists())

        self.assertRedirects(res, self.service_dashboard_url)

    def test_update_service_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service', self.test_service.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_update_service_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload = {
            'company'               : self.test_company.id,
            'service_name'          : 'test service',
            'slug'                  : 'test_service',
            'service_description'   : 'my test service',
            'image'                 : photo_file
        }

        res = self.client.post(
            url_with_args('update_service', self.test_service.id),
            payload,
            format='multipart'
        )
        # print(res.context['form'].errors)

        self.assertEquals(res.status_code, 302)
        self.test_company.refresh_from_db()
        self.assertEqual(str(self.test_service), payload['service_name'])
        self.assertRedirects(res, self.service_dashboard_url)

    def test_delete_service(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        test_service = Service.objects.create(
            company             = self.test_company,
            service_name        = 'test service three',
            slug                = 'test_service_three',
            service_description =  'my test service'
        )

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_service', test_service.id))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.service_dashboard_url)
        self.assertFalse(Company.objects.filter(email='test@testcompany2.com').exists())

    def test_SPD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.SPD_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_SPD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        SPD_res = self.client.post(self.SPD_url, {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'process_name'          : 'test process',
            'process_description'   : 'my test process',
            'image'                 : photo_file,
        }, format='multipart')
        # test_sdp = ServiceProcess.objects.all()[1]
        # print(test_sdp.id)

        self.assertEquals(SPD_res.status_code, 302)
        self.assertTrue(Service.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(ServiceProcess.objects.filter(service_id=self.test_service.id).exists())
        self.assertRedirects(SPD_res, self.SPD_url)

    def test_update_service_process_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service_process', self.test_service_process.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_update_service_process_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload ={
            'company'               :  self.test_company.id,
            'service'               :  self.test_service.id,
            'process_name'          : 'test process',
            'process_description'   : 'my test process',
            'image'                 :  photo_file,
        }

        res = self.client.post(
            url_with_args('update_service_process', self.test_service_process.id),
            payload,
            format='multipart'
        )

        self.assertEquals(res.status_code, 302)
        self.test_service_process.refresh_from_db()
        self.assertRedirects(res, self.SPD_url)

    def test_delete_service_process(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        process = ServiceProcess.objects.all()[0]

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        # print(process.id)

        res = self.client.get(url_with_args(
            'delete_service_process',
            self.test_service_process.id
        ))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.SPD_url)
        self.assertFalse(
            ServiceProcess.objects.filter(id=self.test_service_process.id).exists()
        )
    
    def test_USD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.USD_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/user_subService_dashboard.html')

    def test_USD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        USD_res = self.client.post(self.USD_url, {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user.id,
            'description'           : 'test description',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        })

        self.assertEquals(USD_res.status_code, 302)
        self.assertTrue(Service.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(SubServiceType.objects.filter(service_id=self.test_service.id).exists())
        self.assertTrue(SubService.objects.filter(subServiceType_id=self.test_subservice_type.id).exists())
        self.assertRedirects(USD_res, self.USD_url)

 
def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/services')
    files = [i for i in os.listdir(images_path)
            if os.path.isfile(os.path.join(images_path, i))
            and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))

    sp_images_path = os.path.join(settings.MEDIA_ROOT, 'photos/service_process')
    files = [i for i in os.listdir(sp_images_path)
            if os.path.isfile(os.path.join(sp_images_path, i))
            and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(sp_images_path, file))

    logos_images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    logos_files = [i for i in os.listdir(logos_images_path)
             if os.path.isfile(os.path.join(logos_images_path, i))
             and i.startswith('test_')]

    for file in logos_files:
        os.remove(os.path.join(logos_images_path, file))
