from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from django.urls import reverse, resolve
from staff.views import (
    staff_dashboard, update_staff, delete_staff
)

from accounts.models import Account
from company.models import Company
from staff.models import Staff

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def url_with_args(name, args):
    return reverse(name, args=[args]) 

class TestUrls(TestCase):

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
        self.test_staff = Staff.objects.create(
            company         = self.test_company,
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
        ) 

    def test_staff_dashboard_urls_resolves(self):
        url = reverse('staff_dashboard')
        self.assertEquals(resolve(url).func, staff_dashboard)

    def test_update_staff_urls_resolves(self):
        url = url_with_args('update_staff', self.test_staff.id)
        self.assertEquals(resolve(url).func, update_staff)
    
    def test_delete_staff_urls_resolves(self):
        url = url_with_args('delete_staff', self.test_staff.id)
        self.assertEquals(resolve(url).func, delete_staff)

