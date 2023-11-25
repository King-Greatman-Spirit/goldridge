from django.test import TestCase
from django.urls import reverse, resolve
from service.views import (
   service, service_dashboard, update_service, delete_service, service_process_dashboard, 
   update_service_process, delete_service_process, user_subService_dashboard
)
from accounts.models import Account
from company.models import Company
from service.models import (
    Service, ServiceProcess, Testimonial, 
    SubServiceType, SubService, Prerequisite, Transaction
)

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
        self.test_service = Service.objects.create(
            company             = self.test_company,
            service_name        = 'test service',
            slug                = 'test_service',
            service_description =  'my test service'
        )
        self.test_service_process = ServiceProcess.objects.create(
            company               = self.test_company,
            service               = self.test_service,
            process_name          = 'test process',
            process_description   = 'my test process'
        )
        self.test_subservice_type = SubServiceType.objects.create(
            company               = self.test_company,
            service               = self.test_service,
            type                  = 'test type',
            description           = 'test description'
        )
        self.test_user_subservice    = SubService.objects.create(
            company                  = self.test_company,
            service                  = self.test_service,
            subServiceType           = self.test_subservice_type,
            user                     = self.user,
            description              = 'test description',
            duration                 = 6,
            rate                     = 3,
            target                   = 5000
        )

    def test_service_urls_resolves(self):
        url = url_with_args('service_slug', self.test_service.slug)
        self.assertEquals(resolve(url).func, service)

    def test_service_dashboard_urls_resolves(self):
        url = reverse('service_dashboard')
        self.assertEquals(resolve(url).func, service_dashboard)

    def test_update_service_urls_resolves(self):
        url = url_with_args('update_service', self.test_service.id)
        self.assertEquals(resolve(url).func, update_service)

    def test_delete_service_urls_resolves(self):
        url = url_with_args('delete_service', self.test_service.id)
        self.assertEquals(resolve(url).func, delete_service)

    def test_service_process_dashboard_urls_resolves(self):
        url = reverse('service_process_dashboard')
        self.assertEquals(resolve(url).func, service_process_dashboard)

    def test_update_service_process_urls_resolves(self):
        url = url_with_args('update_service_process', self.test_service.id)
        self.assertEquals(resolve(url).func, update_service_process)

    def test_delete_service_process_urls_resolves(self):
        url = url_with_args('delete_service_process', self.test_service.id)
        self.assertEquals(resolve(url).func, delete_service_process)

    def test_user_subService_dashboard_urls_resolves(self):
        url = reverse('user_subService_dashboard')
        self.assertEquals(resolve(url).func, user_subService_dashboard)

