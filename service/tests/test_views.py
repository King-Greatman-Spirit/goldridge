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

def custom_args(name, service_id, app_id):
    return reverse(name, args=[service_id, app_id])



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.service_dashboard_url = reverse('service_dashboard')
        self.SPD_url = reverse('service_process_dashboard')
        self.company_dashboard_url = reverse('company_dashboard')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.admin_login_url = reverse('admin_login')
        self.ASA_url = reverse('admin_service_applications')
        self.USA_url = reverse('user_service_applications')
        self.ABT_url = reverse('apps-by-type')
        self.CT_url = reverse('clients-table')
        self.STD_url = reverse('subservice-type-dashboard')
        self.setUp_file = generate_photo_file()
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
        self.user2 = Account.objects.create_user(
            first_name = 'first2',
            last_name = 'last2',
            email = 'user2@example.com',
            password = 'testpass5678',
            username = 'first2_last2'
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
            abbr                  = 'test abbr',
            description           = 'test description'
        )
        self.test_service_application  = SubService.objects.create(
            company                           = self.test_company,
            service                           = self.test_service,
            subServiceType                    = self.test_subservice_type,
            user                              = self.user,
            description                       = 'test description',
            approval                          = approval_chioce[3][0],
            approval_note                     = 'test note',
            duration                          = 6,
            rate                              = 3,
            target                            = 5000
        )
        self.test_app = SubService.objects.create(
            company                           = self.test_company,
            service                           = self.test_service,
            subServiceType                    = self.test_subservice_type,
            user                              = self.user,
            description                       = 'description test',
            approval                          = approval_chioce[3][0],
            approval_note                     = 'test approval',
            duration                          = 6,
            rate                              = 3,
            target                            = 5000
        )
        self.type_dashboard_url = reverse('type-dashboard', args=[self.test_service_application.service.id])
        self.update_service_url = reverse('update_service', args=[self.test_service.id])
        self.delete_service_url = reverse('delete_service', args=[self.test_service.id])
        self.update_service_process_url = reverse('update_service_process', args=[self.test_service_process.id])
        self.delete_service_process_url = reverse('delete_service_process', args=[self.test_service_process.id])
        self.Update_ASA_url = reverse('update_admin_service_app', args=[self.test_service_application.id])
        self.delete_ASA_url = reverse('delete_admin_service_app', args=[self.test_service_application.id])
        self.Update_TD_url = reverse('update-type-dashboard', args=[self.test_service.id, self.test_app.id])
        self.delete_TD_url = reverse('delete-type-dashboard', args=[self.test_service_application.id])
        self.update_STD_url = reverse('update-subservice-type', args=[self.test_subservice_type.id])
        self.delete_STD_url = reverse('delete-subservice-type', args=[self.test_subservice_type.id])



    def test_service(self):
        res = self.client.get(url_with_args('service_slug',  self.test_service.slug))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service.html')


    def test_service_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.service_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_service_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service', self.test_service.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_update_service_POST(self):
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
        test_user.is_admin = True
        test_user.save()

        test_service = Service.objects.create(
            company             = self.test_company,
            service_name        = 'test service three',
            slug                = 'test_service_three',
            service_description =  'my test service'
        )

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.SPD_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_SPD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service_process', self.test_service_process.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_update_service_process_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
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
        test_user.is_admin = True
        test_user.save()

        process = ServiceProcess.objects.all()[0]

        admin_login_res = self.client.post(self.admin_login_url, {
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
    
    def test_USA_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.USA_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/user_subService_dashboard.html')

    def test_USA_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        test_user2 = Account.objects.get(email='user2@example.com')
        test_user2.is_active = True
        test_user2.save()

        # Login user1
        self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        # Submit SubService application for user1
        USA_res_user1 = self.client.post(self.USA_url, {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user.id,
            'description'           : 'test description user1',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        })

        # Assertions for user1 submission
        self.assertEquals(USA_res_user1.status_code, 302)
        self.assertTrue(SubService.objects.filter(description='test description user1').exists())
        self.assertRedirects(USA_res_user1, self.USA_url)

        # Login user2
        self.client.post(self.login_url, {
            'email' : 'user2@example.com',
            'password': 'testpass5678'
        })

        # Submit SubService application for user2
        USA_res_user2 = self.client.post(self.USA_url, {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user2.id,
            'description'           : 'test description user2',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        })

        # Assertions for user2 submission
        self.assertEquals(USA_res_user2.status_code, 302)
        self.assertTrue(SubService.objects.filter(description='test description user2').exists())
        self.assertRedirects(USA_res_user2, self.USA_url)

        # Get the SubService instances
        sub_service_user1 = SubService.objects.get(description='test description user1')
        sub_service_user2 = SubService.objects.get(description='test description user2')

        # Assert that the char_id values are unique
        self.assertNotEquals(sub_service_user1.char_id, sub_service_user2.char_id)

        self.assertTrue(Service.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(SubServiceType.objects.filter(service_id=self.test_service.id).exists())
        self.assertTrue(SubService.objects.filter(subServiceType_id=self.test_subservice_type.id).exists())
        


    def test_ASA_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })


        res = self.client.get(self.ASA_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/admin_subService_dashboard.html')

    def test_Update_ASA_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_admin_service_app', self.test_service_application.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/admin_subService_dashboard.html')

    def test_Update_ASA_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload ={
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user.id,
            'description'           : 'test description',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        }

        res = self.client.post(
            url_with_args('update_admin_service_app', self.test_service_application.id),
            payload
        )

        self.assertEquals(res.status_code, 302)
        self.test_service_application.refresh_from_db()
        self.assertEqual(self.test_service_application.duration, payload['duration'])
        self.assertRedirects(res, self.ASA_url)

    def test_delete_ASA(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args(
            'delete_admin_service_app',
            self.test_service_application.id
        ))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.ASA_url)
        self.assertFalse(
            SubService.objects.filter(id=self.test_service_application.id).exists()
        )

    def test_apps_by_type_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        res = self.client.get(self.ABT_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/app_by_type/app_by_type.html')

    def test_type_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        res = self.client.get(url_with_args('type-dashboard',  self.test_service.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/app_by_type/type_dashboard.html')

    def test_type_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload ={
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user.id,
            'description'           : 'test description',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        }

        res = self.client.post(
            url_with_args('type-dashboard', self.test_service.id),
            payload
        )

        self.assertEquals(res.status_code, 302)
        self.test_service_application.refresh_from_db()
        self.assertEqual(self.test_service_application.duration, payload['duration'])
        self.assertRedirects(res, self.type_dashboard_url)

    def test_delete_TD(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args(
            'delete-type-dashboard',
            self.test_service_application.id
        ))
        # Check if the view returns a redirect status code
        self.assertEquals(res.status_code, 302)

        # Check if the view redirects to the correct URL
        self.assertRedirects(res, reverse('type-dashboard', args=[self.test_service_application.service.id]))

        # Check if the SubService object has been deleted
        self.assertFalse(SubService.objects.filter(id=self.test_service_application.id).exists())

    def test_Update_TD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        # Assuming you have a test_service_application instance
        res = self.client.get(
            custom_args('update-type-dashboard', self.test_service.id, self.test_app.id)
        )


        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/app_by_type/type_dashboard.html')

    def test_Update_TD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload ={
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'subServiceType'        : self.test_subservice_type.id,
            'user'                  : self.user.id,
            'description'           : 'test description',
            'approval'              : approval_chioce[3][0],
            'duration'              : 6,
            'rate'                  : 3,
            'target'                : 5000,
        }

        res = self.client.post(
            custom_args('update-type-dashboard', self.test_service.id, self.test_app.id),
            payload 
        )

        self.assertEquals(res.status_code, 302)
        self.test_service_application.refresh_from_db()
        self.assertEqual(self.test_service_application.duration, payload['duration'])
        self.assertRedirects(res, self.type_dashboard_url)

    def test_clients_table_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        res = self.client.get(self.CT_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/admin/clients_table.html')

    def test_STD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.STD_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/subservice_type_dashboard.html')

    def test_STD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        STD_res = self.client.post(self.STD_url, {
            'company'             : self.test_company.id,
            'service'             : self.test_service.id,
            'type'                : 'test type',
            'abbr'                : 'test abbreviation',
            'description'         : 'test description'
        })

        self.assertEquals(STD_res.status_code, 302)
        self.assertTrue(Service.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(SubServiceType.objects.filter(service_id=self.test_service.id).exists())
        self.assertRedirects(STD_res, self.STD_url)

    def test_update_STD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update-subservice-type', self.test_subservice_type.id))

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/subservice_type_dashboard.html')

    def test_update_STD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        payload ={
            'company'             :  self.test_company.id,
            'service'             : self.test_service.id,
            'type'                : 'test type',
            'abbr'                : 'test abbreviation',
            'description'         : 'test description'
        }

        res = self.client.post(
            url_with_args('update-subservice-type', self.test_subservice_type.id),
            payload
        )

        self.assertEquals(res.status_code, 302)
        self.test_subservice_type.refresh_from_db()
        self.assertRedirects(res, self.STD_url)

    def test_delete_STD(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args(
            'delete-subservice-type',
            self.test_subservice_type.id
        ))

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.STD_url)
        self.assertFalse(
            SubServiceType.objects.filter(id=self.test_subservice_type.id).exists()
        )

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

        # Try to access the service dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.service_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the service dashboard
        self.assertEquals(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.service_dashboard_url))  # Ensure not redirected to service dashboard view

        # Try to access the update service view as a client
        res_update = self.client.get(self.update_service_url)

        # Check that the client is redirected to the login page when attempting to access the update service view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_service_url))  # Ensure not redirected to update service view

        # Try to access the delete service view as a client
        res_delete = self.client.get(self.delete_service_url)

        # Check that the client is redirected to the login page after attempting to access the delete service view
        self.assertEquals(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_service_url))  # Ensure not redirected to delete service view

        # Try to access the SPD view as a client
        res_spd = self.client.get(self.SPD_url)

        # Check that the client is redirected to the login page when attempting to access the SPD view
        self.assertEquals(res_spd.status_code, 302)
        self.assertFalse(res_spd.url.startswith(self.SPD_url))  # Ensure not redirected to SPD view

        # Try to access the update service process view as a client
        res_update = self.client.get(self.update_service_process_url)

        # Check that the client is redirected to the login page when attempting to access the update service process view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_service_process_url))  # Ensure not redirected to update service process view

        # Try to access the delete service process view as a client
        res_delete = self.client.get(self.delete_service_process_url)

        # Check that the client is redirected to the login page after attempting to access the delete service process view
        self.assertEquals(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_service_process_url))  # Ensure not redirected to delete service process view

        # Try to access the ASA view as a client
        res_asa = self.client.get(self.ASA_url)

        # Check that the client is redirected to the login page when attempting to access the ASA view
        self.assertEquals(res_asa.status_code, 302)
        self.assertFalse(res_asa.url.startswith(self.ASA_url))  # Ensure not redirected to ASA view

        # Try to access the update ASA view as a client
        res_update = self.client.get(self.Update_ASA_url)

        # Check that the client is redirected to the login page when attempting to access the update ASA view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.Update_ASA_url))  # Ensure not redirected to update ASA view

        # Try to access the delete ASA view as a client
        res_delete = self.client.get(self.delete_ASA_url)

        # Check that the client is redirected to the login page after attempting to access the delete ASA view
        self.assertEquals(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_ASA_url))  # Ensure not redirected to delete ASA view

        # Try to access the ABT view as a client
        res_abt = self.client.get(self.ABT_url)

        # Check that the client is redirected to the login page when attempting to access the update ABT view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.ABT_url))  # Ensure not redirected to update TD view

        # Try to access the delete TD view as a client
        res_dashboard = self.client.get(self.type_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the delete TD view
        self.assertEquals(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.type_dashboard_url))  # Ensure not redirected to delete TD view

        # Try to access the update TD view as a client
        res_update = self.client.get(self.Update_TD_url)

        # Check that the client is redirected to the login page when attempting to access the update TD view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.Update_TD_url))  # Ensure not redirected to update TD view

        # Try to access the delete TD view as a client
        res_delete = self.client.get(self.delete_TD_url)

        # Check that the client is redirected to the login page after attempting to access the delete TD view
        self.assertEquals(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_TD_url))  # Ensure not redirected to delete TD view

        # Try to access the CT view as a client
        res_ct = self.client.get(self.CT_url)

        # Check that the client is redirected to the login page after attempting to access the CT view
        self.assertEquals(res_ct.status_code, 302)
        self.assertFalse(res_ct.url.startswith(self.CT_url))  # Ensure not redirected to CT view

        # Try to access the update TD view as a client
        res_dashboard = self.client.get(self.STD_url)

        # Check that the client is redirected to the login page when attempting to access the update TD view
        self.assertEquals(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.STD_url))  # Ensure not redirected to update TD view

        # Try to access the delete TD view as a client
        res_update = self.client.get(self.update_STD_url)

        # Check that the client is redirected to the login page after attempting to access the delete TD view
        self.assertEquals(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_STD_url))  # Ensure not redirected to delete TD view

        # Try to access the CT view as a client
        res_delete = self.client.get(self.delete_STD_url)

        # Check that the client is redirected to the login page after attempting to access the CT view
        self.assertEquals(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_STD_url))  # Ensure not redirected to CT view

 
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
