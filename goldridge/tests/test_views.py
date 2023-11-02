# import os
# import io
# import shutil
# from django.conf import settings
# from django.core.files.base import ContentFile

# from PIL import Image

# from django.test import TestCase, Client
# from django.urls import reverse

# from accounts.models import Account
# from company.models import Company, CompanyOverview
# from service.models import Service, ServiceProcess
# from staff.models import Staff

# from django.utils import timezone
# from datetime import datetime

# from django.conf.urls import handler404, handler500

# def generate_photo_file():
#     file = io.BytesIO()
#     image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
#     image.save(file, 'png')
#     file.name = 'test_image.png'
#     file.seek(0)
#     return file

# def url_with_args(name, args):
#     return reverse(name, args=[args])

# class TestViews(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.home_url = reverse('home')
#         self.user = Account.objects.create_user(
#             first_name = 'first',
#             last_name = 'last',
#             email = 'user1@example.com',
#             password = 'testpass1234',
#             username = 'first_last'
#         )
#         # Create a company with id=1 and is_client=False
#         self.test_company = Company.objects.create(
#             id=1,
#             company_name = 'testcompany',
#             website_address = 'http://testcompany.com',
#             email = 'test@testcompany.com',
#             address_line_1 = 'address line 1',
#             city = 'test city',
#             state = 'test state',
#             postal_code = '111222',
#             country = 'test country',
#             phone = '11122233344',
#             user = self.user
#         )
#         self.test_company_overview = CompanyOverview.objects.create(
#             company = self.test_company,
#             business_overview = 'test business overview',
#             competive_advantage = 'test competitive advantage',
#             mission_statement = 'test mission statement',
#             vision = 'test vision',
#             philosophy = 'test philosophy'
#         )
#         self.setUp_file = generate_photo_file()
#         self.test_service = Service.objects.create(
#             company             = self.test_company,
#             service_name        = 'test service',
#             slug                = 'test_service',
#             service_description = 'Testing service description',
#             image               = ContentFile(self.setUp_file.read(), 'test_image.png')
#         )
#         self.test_service_process = ServiceProcess.objects.create(
#             company             = self.test_company,
#             service             = self.test_service,
#             process_name        = 'test process',
#             process_description = 'my test process',
#             image               = ContentFile(self.setUp_file.read(), 'test_image.png')
#         )
#         self.test_staff = Staff.objects.create(
#             company         = self.test_company,
#             first_name      = 'test first',
#             last_name       = 'test last',
#             job_title       = 'test job',
#             about           = 'my test about',
#             phone           =  '11122233344',
#             email           = 'test@teststaff.com',
#             address_line_1  = 'address line 1',
#             city            = 'test city',
#             state           = 'test state',
#             country         = 'test country',
#             photo = ContentFile(self.setUp_file.read(), 'test_image.png'),
#             employment_date = timezone.now()
#         )


#     def test_home(self):
#         res = self.client.get(self.home_url)

#         self.assertEquals(res.status_code, 200)
#         self.assertTemplateUsed(res, 'home.html')

#     # def test_error_500(self):
#     #     self.client.raise_request_exception = False
#     #     res = self.client.get(reverse(handler500))
#     #     print(handler500.__dir__())
#     #     self.assertEqual(res.status_code, 500)
#     #     self.assertTrue('Sorry the Page Could not be Found' in res.content.decode('utf8'))

# def tearDownModule():
#     images_path = os.path.join(settings.MEDIA_ROOT, 'photos/services')
#     files = [i for i in os.listdir(images_path)
#             if os.path.isfile(os.path.join(images_path, i))
#             and i.startswith('test_')]

#     for file in files:
#         os.remove(os.path.join(images_path, file))
 
#     sp_images_path = os.path.join(settings.MEDIA_ROOT, 'photos/service_process')
#     files = [i for i in os.listdir(sp_images_path)
#             if os.path.isfile(os.path.join(sp_images_path, i))
#             and i.startswith('test_')]

#     for file in files:
#         os.remove(os.path.join(sp_images_path, file))
