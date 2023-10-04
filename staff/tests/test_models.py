from django.test import TestCase
from django.utils import timezone
from datetime import datetime


from company.models import Company
from staff.models import Staff


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


def create_staff(
    company,
    first_name      = 'test first',
    last_name       = 'test last',
    job_title       = 'test job',
    about           = 'my test about',
    phone           =  '11122233344',
    email           = 'test@teststaff.com',
    address_line_1  = 'address line 1',
    city            = 'test city',
    state           = 'test state',
    country         = 'test country',
    # employment_date = datetime(2022, 12, 7, 11, 30, 11, 429000)
    employment_date = timezone.now()
):
    return Staff.objects.create(
        company         = company,
        first_name      = first_name,
        last_name       = last_name,
        job_title       = job_title,
        about           = about,
        phone           = phone,
        email           = email,
        address_line_1  = address_line_1,
        city            = city,
        state           = state,
        country         = country,
        employment_date = employment_date
    )


class TestModels(TestCase):
    def test_create_staff(self):
        first_name      = 'test first'
        phone           = '11122233344'
        email           = 'test@teststaff.com'

        company = create_company()
        staff = create_staff(company)

        self.assertEquals(str(staff), first_name)
        self.assertEquals(staff.phone, phone)
        self.assertEquals(staff.email, email)
        self.assertTrue(staff.is_active)
        self.assertFalse(staff.is_management)
        self.assertFalse(staff.is_primary_contact)
