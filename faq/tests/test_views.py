from django.test import TestCase, Client
from django.urls import reverse

from faq.models import FAQ, FAQCategory
from faq.forms import FAQForm

from accounts.models import Account
from company.models import Company  # Import your Company model

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.faq_list_url = reverse('faq_list')

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
            user = self.user
        )
        
        # Create a test category
        self.test_category = FAQCategory.objects.create(
            name='Test Category'
        )

        # Create a FAQ in the test category
        self.test_faq = FAQ.objects.create(
            category=self.test_category,
            question='Test Question',
            answer='Test Answer',
        )

        # Modify this line to set the faq_detail_url
        self.faq_detail_url = reverse('faq_detail', args=[self.test_category.id])

    def test_faq_list_GET(self):
        res = self.client.get(self.faq_list_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/faq_list.html')

    def test_faq_detail_GET(self):
        res = self.client.get(self.faq_detail_url)  # Use the faq_detail_url

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/faq_detail.html')

    def test_faq_detail_GET_invalid_category(self):
        url = reverse('faq_detail', args=[999])  # Use an invalid category ID
        res = self.client.get(url)

        self.assertEquals(res.status_code, 404)

    def test_faq_list_POST(self):
        res = self.client.post(self.faq_list_url, {
            'category': self.test_category.id,
            'question': 'Test Question 2',
            'answer': 'Test Answer 2',
        })

        self.assertEquals(res.status_code, 302)
        self.assertTrue(FAQ.objects.filter(question='Test Question 2').exists())
        self.assertRedirects(res, self.faq_list_url)

    def test_faq_list_POST_invalid_data(self):
        # Create a form instance with invalid data
        form_data = {
            'category': self.test_category.id,
            'question': '',  # Empty question to trigger validation error
            'answer': '',    # Empty answer to trigger validation error
        }
        invalid_form = FAQForm(data=form_data)  # Use the FAQForm to create the form instance

        # Simulate a POST request with the invalid form data
        res = self.client.post(self.faq_list_url, form_data)

        self.assertEquals(res.status_code, 200)
        self.assertFormError(res, 'form', 'question', 'This field is required.')
        self.assertFormError(res, 'form', 'answer', 'This field is required.')

