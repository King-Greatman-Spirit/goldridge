from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from company.models import Company
from service.models import (
    Service, ServiceProcess, Testimonial, SubServiceType, 
    SubService, Prerequisite, Transaction, transactionType_chioce, approval_chioce
)
from accounts.models import Account

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

def create_testimonial(
    company,
    service,
    description        = 'test description',
    client_full_name   = 'test full name',
    client_location    = 'test location'
):
    return Testimonial.objects.create(
        company             = company,
        service             = service,
        description         = description,
        client_full_name    = client_full_name,
        client_location     = client_location
    )

def create_subservice_type(
    company,
    service,
    type          = 'test type',
    description   = 'test description'
):
    return SubServiceType.objects.create(
        company      = company,
        service      = service,
        type         = type,
        description  = description
    )

def create_user(
    first_name = 'first',
    last_name = 'last',
    email = 'user1@example.com',
    password = 'testpass1234',
    username = 'first_last'  
):
    return Account.objects.create(
        first_name = first_name,
        last_name  = last_name,
        email      = email,
        password   = password,
        username   = username
    )

def create_subservice(
    company,
    service,
    subServiceType,
    user,
    description   = 'test description',
    approval      = approval_chioce[3][0],
    approval_note = 'test note',
    duration      = 6,
    rate          = 3,
    target        = 5000
):
    return SubService.objects.create(
        company        = company,
        service        = service,
        subServiceType = subServiceType,
        user           = user,
        description    = description,
        approval       = approval,
        approval_note  = approval_note,
        duration       = duration,
        rate           = rate,
        target         = target
    )

def create_prerequisite(
    company,
    service,
    subServiceType,
    prerequisite   = 'test prerequisite',
    description = 'test description'
):
    return Prerequisite.objects.create(
        company        = company,
        service        = service,
        subServiceType = subServiceType,
        prerequisite   = prerequisite,
        description    = description
    )

def create_transaction(
    company,
    service,
    subServiceType,
    user,
    amount = 2000,
    transactionType = transactionType_chioce[2][0],
    user_email      = 'test@testuser.com'
):
    return Transaction.objects.create(
        company         = company,
        service         = service,
        subServiceType  = subServiceType,
        user            = user,
        amount          = amount,
        transactionType = transactionType,
        user_email      = user_email
    )


class TestModels(TestCase):
    def test_create_service(self):
        service_name        = 'test service'
        slug                = 'test_service'
        service_description = 'my test service'

        company = create_company()
        service = create_service(company)

        self.assertEquals(str(service), service_name)
        self.assertEquals(service.slug, slug)
        self.assertEquals(service.service_description, service_description)

    def test_create_service_process(self):
        process_name        = 'test process'
        process_description = 'my test process'

        company = create_company()
        service = create_service(company)
        service_process = create_service_process(company, service)

        self.assertEquals(str(service_process), process_name)
        self.assertEquals(service_process.process_description, process_description)

    def test_create_testimonial(self):
        description        = 'test description'
        client_full_name   = 'test full name'
        client_location    = 'test location'

        company = create_company()
        service = create_service(company)
        testimonial = create_testimonial(company, service)

        self.assertEquals(str(testimonial), description)
        self.assertEquals(testimonial.client_full_name, client_full_name)
        self.assertEquals(testimonial.client_location, client_location)

    def test_create_subservice_type(self):
        type          = 'test type'
        description   = 'test description'

        company = create_company()
        service = create_service(company)
        subservice_type = create_subservice_type(company, service)

        self.assertEquals(str(subservice_type), type)
        self.assertEquals(subservice_type.description, description)

    def test_create_subservice(self):
        description   = 'test description'
        approval_note = 'test note'
        duration      = 6
        target        = 5000

        company = create_company()
        service = create_service(company)
        user    = create_user()
        subservice_type = create_subservice_type(company, service)
        subservice = create_subservice(company, service, subservice_type, user)

        self.assertEquals(subservice.duration, duration)
        self.assertEquals(subservice.description, description)
        self.assertEquals(subservice.approval_note, approval_note)
        self.assertEquals(subservice.target, target)

    def test_create_prerequisite(self):
        prerequisite   = 'test prerequisite'
        description    = 'test description'

        company = create_company()
        service = create_service(company)
        subservice_type = create_subservice_type(company, service)
        prerequisites = create_prerequisite(company, service, subservice_type)

        self.assertEquals(str(prerequisites), prerequisite)
        self.assertEquals(prerequisites.description, description)

    def test_create_transaction(self):
        amount          = 2000
        transactionType = transactionType_chioce[2][0]
        user_email      = 'test@testuser.com'

        company = create_company()
        service = create_service(company)
        user    = create_user()
        subservice_type = create_subservice_type(company, service)
        transaction = create_transaction(company, service, subservice_type, user)

        self.assertEquals(transaction.amount, amount)
        self.assertEquals(transaction.user_email, user_email)
        self.assertEquals(transaction.transactionType, transactionType)
