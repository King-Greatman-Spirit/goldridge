from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from company.models import Company
from service.models import Service, ServiceProcess
from faq.models import FAQCategory, FAQ

def create_company(
    company_name    = 'test company',
    website_address = 'http://testcompany.com',
    email           = 'test@testcompany.com',
    address_line_1  = 'address line 1',
    city            = 'test city',
    state           = 'test state',
    postal_code     = 'test code',
    country         = 'test country',
    phone           = 'testphone'
):
    return Company.objects.create(
        company_name    = company_name,
        website_address = website_address,
        email           = email,
        address_line_1  = address_line_1,
        city            = city,
        state           = state,
        postal_code     = postal_code,
        country         = country,
        phone           = phone
    )

def create_service(
    company,
    service_name        = 'test service',
    slug                = 'test_service',
    service_description =  'my test service'
):
    return Service.objects.create(
        company             = company,
        service_name        = service_name,
        slug                = slug,
        service_description  = service_description
    )

def create_service_process(
    company,
    service,
    process_name        = 'test process',
    process_description = 'my test process'
):
    return ServiceProcess.objects.create(
        company             = company,
        service             = service,
        process_name        = process_name,
        process_description  = process_description
    )

class TestFAQModels(TestCase):

    def test_create_faq_category(self):
        category_name = 'Test Category'

        category = FAQCategory.objects.create(name=category_name)

        self.assertEqual(str(category), category_name)

    def test_create_faq(self):
        category_name = 'Test Category'
        question = 'Test Question'
        answer = 'Test Answer'

        company = create_company()
        service = create_service(company)

        category = FAQCategory.objects.create(name=category_name)
        faq = FAQ.objects.create(
            category=category,
            service=service,
            question=question,
            answer=answer
        )

        self.assertEqual(str(faq), question)
        self.assertEqual(faq.category, category)
        self.assertEqual(faq.service, service)
        self.assertEqual(faq.answer, answer)
