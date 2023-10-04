from django.test import TestCase
from company.models import Company
from service.models import Service
from enquiry.models import Lead, Newsletter, no_of_employees_chioce, channel_chioce


def create_company(
    company_name = 'testcompany',
    website_address = 'http://testcompany.com',
    email = 'test@testcompany.com',
    address_line_1 = 'address line 1',
    city = 'test city',
    state = 'test state',
    postal_code = 'test code',
    country = 'test country',
    phone = 'testphone'
):
    return Company.objects.create(
        company_name = company_name,
        website_address = website_address,
        email = email,
        address_line_1 = address_line_1,
        city = city,
        state = state,
        postal_code = postal_code,
        country = country,
        phone = phone
    )

def create_service(company, service_name = 'Test name', slug = 'test_name'):
    return Service.objects.create(
        company = company,
        service_name = service_name,
        slug = slug
    )


def create_enquiry(
    service,
    full_name = 'test full',
    email = 'test@testlead.com',
    phone_number = '2348176334125',
    company_name = 'test company',
    no_of_employees = no_of_employees_chioce[3][0],
    message = 'my test message',
    channel = channel_chioce[3][0]
):
    return Lead.objects.create(
        service = service,
        full_name = full_name,
        phone_number= phone_number,
        email = email,
        company_name = company_name,
        no_of_employees = no_of_employees,
        message = message,
        channel = channel
    )

def create_lead(
    full_name = 'test full',
    email = 'test@testlead.com',
    phone_number = '2348176334125'

):
    return Newsletter.objects.create(
        full_name = full_name,
        phone_number= phone_number,
        email = email
    )


class TestModels(TestCase):

    def test_create_enquiry(self):
        full_name = 'test full'
        email = 'test@testlead.com'
        no_of_employees = no_of_employees_chioce[3][0]
        channel = channel_chioce[3][0]

        company = create_company()
        service = create_service(company)
        enquiry = create_enquiry(service)

        self.assertEquals(str(enquiry), email)
        self.assertEquals(enquiry.full_name, full_name)
        self.assertEquals(enquiry.no_of_employees, no_of_employees)
        self.assertEquals(enquiry.channel, channel)

    def test_create_lead(self):
        full_name = 'test full'
        email = 'test@testlead.com'

        lead = create_lead()

        self.assertEquals(str(lead), email)
        self.assertEquals(lead.full_name, full_name)
