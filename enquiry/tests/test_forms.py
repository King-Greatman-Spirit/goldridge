from django.test import TestCase
from enquiry.forms import EnquiryForm, LeadForm
from accounts.models import Account
from company.models import Company
from service.models import Service
from enquiry.models import Lead, channel_chioce


class TestForms(TestCase):

    def setUp(self):
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
            user = self.user
        )

        self.test_service = Service.objects.create(
            company = self.test_company,
            service_name = 'Test name',
            slug = 'test_name',
        )


    def test_enquiry_form_valid_data(self):
        form = EnquiryForm(data ={
            'full_name': 'test full',
            'email': 'test@testlead.com',
            'phone_number': '2348176334125',
            'company_name': 'test company',
            'service': self.test_service,
            'message': 'my test message',
            'channel': channel_chioce[3][0]
        })

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)


    def test_enquiry_form_no_data(self):

        form = EnquiryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_lead_form_valid_data(self):
        form = LeadForm(data ={
            'full_name': 'test full',
            'email': 'test@testlead.com',
            'phone_number': '2348176334125'
        })

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)


    def test_lead_form_no_data(self):

        form = LeadForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)