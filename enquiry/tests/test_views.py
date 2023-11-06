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
from service.models import Service
from enquiry.models import Lead, channel_chioce

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.contact_us_url = reverse('contact_us')
        self.subscribe_url = reverse('subscribe')
        self.setUp_file = generate_photo_file()
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
            logo = ContentFile(self.setUp_file.read(), 'test_image.png')
        )

        self.test_service = Service.objects.create(
            company = self.test_company,
            service_name = 'Test name',
            slug = 'test_name'
        )


    def test_contact_us_GET(self):
        res = self.client.get(self.contact_us_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'enquiry/contact_us.html')

    def test_contact_us_POST(self):
        res = self.client.post(self.contact_us_url, {
            'full_name': 'test full',
            'email': 'test@testlead.com',
            'phone_number': '2348176334125',
            'company_name': 'test company',
            'service': self.test_service.id,
            'message': 'my test message',
            'channel': channel_chioce[3][0]
        })
        # print(res.context['form'].errors)
        # contact = Lead.objects.get(id=1)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals(contact.email, 'test@testlead.com')
        self.assertRedirects(res, self.contact_us_url)

    def test_subscirbe_GET(self):
        res = self.client.get(self.subscribe_url, {}, HTTP_REFERER='http://foo/bar')

        self.assertEquals(res.status_code, 302)
        # self.assertTemplateUsed(res, 'enquiry/contact.html')

    def test_subscribe_POST(self):
        res = self.client.post(self.subscribe_url, {
            'full_name': 'test full',
            'email': 'test@testlead.com',
            'phone_number': '2348176334125'
        }, HTTP_REFERER='http://foo/bar')
        # print(res.context['form'].errors)
        # contact = Lead.objects.get(id=1)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals(contact.email, 'test@testlead.com')
        # self.assertRedirects(res, self.contact_us_url)

def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))