import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from faq.models import FAQCategory, FAQQuestion
# from faq.forms import FAQForm

from accounts.models import Account
from company.models import Company  # Import your Company model

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
        self.photo_file = generate_photo_file()
        # Create a Account object for testing
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
        # Create a Company object for testing
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

        # Create a test category
        self.test_FAQCategory = FAQCategory.objects.create(
            home_note   = 'test home note',
            name = 'test name'
        )

        # Create a FAQ in the test category
        self.test_FAQQuestion = FAQQuestion.objects.create(
            category=self.test_FAQCategory,
            question='Test Question',
            answer='Test Answer',
        )

        self.FAQCategory_url = reverse('faq_categories')
        self.FAQQuestion_url = reverse('faq_question', args=[self.test_FAQCategory.id])



    def test_faq_categories_GET(self):
        res = self.client.get(self.FAQCategory_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/faq.html')

    def test_faq_question_GET(self):
        res = self.client.get(self.FAQQuestion_url)  # Use the faq_detail_url

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/faq.html')

    def test_FAQQuestion_url_GET_invalid_category(self):
        url = reverse('faq_question', args=[999])  # Use an invalid category ID
        res = self.client.get(url)

        self.assertEquals(res.status_code, 404)

    # def test_faq_list_POST(self):
    #     res = self.client.post(self.faq_list_url, {
    #         'category': self.test_category.id,
    #         'question': 'Test Question 2',
    #         'answer': 'Test Answer 2',
    #     })

    #     self.assertEquals(res.status_code, 302)
    #     self.assertTrue(FAQ.objects.filter(question='Test Question 2').exists())
    #     self.assertRedirects(res, self.faq_list_url)

    # def test_faq_list_POST_invalid_data(self):
    #     # Create a form instance with invalid data
    #     form_data = {
    #         'category': self.test_category.id,
    #         'question': '',  # Empty question to trigger validation error
    #         'answer': '',    # Empty answer to trigger validation error
    #     }
    #     invalid_form = FAQForm(data=form_data)  # Use the FAQForm to create the form instance

    #     # Simulate a POST request with the invalid form data
    #     res = self.client.post(self.faq_list_url, form_data)

    #     self.assertEquals(res.status_code, 200)
    #     self.assertFormError(res, 'form', 'question', 'This field is required.')
    #     self.assertFormError(res, 'form', 'answer', 'This field is required.')

def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
            if os.path.isfile(os.path.join(images_path, i))
            and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))

