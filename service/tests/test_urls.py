from django.test import TestCase
from django.urls import reverse, resolve
from service.views import (
   service, service_dashboard, update_service, delete_service, service_process_dashboard, 
   update_service_process, delete_service_process, user_subService_dashboard,
   admin_subService_dashboard, update_admin_subService, delete_admin_subService,
   apps_by_type, type_dashboard, delete_type_dashboard, update_type_dashboard, clients_table,
   subservice_type_dashboard, update_subservice_type, delete_subservice_type
)
from accounts.models import Account
from company.models import Company
from service.models import (
    Service, ServiceProcess, Testimonial, SubServiceType, 
    SubService, Prerequisite, Transaction, approval_chioce
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
            abbr                  = 'test abbr',
            description           = 'test description'
        )
        self.test_service_application    = SubService.objects.create(
            company                      = self.test_company,
            service                      = self.test_service,
            subServiceType               = self.test_subservice_type,
            user                         = self.user,
            description                  = 'test description',
            approval                     = approval_chioce[3][0],
            approval_note                = 'test note',
            duration                     = 6,
            rate                         = 3,
            target                       = 5000
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

    def test_user_service_applications_urls_resolves(self):
        url = reverse('user_service_applications')
        self.assertEquals(resolve(url).func, user_subService_dashboard)

    def test_admin_service_applications_urls_resolves(self):
        url = reverse('admin_service_applications')
        self.assertEquals(resolve(url).func, admin_subService_dashboard)

    def test_update_admin_service_app_urls_resolves(self):
        url = url_with_args('update_admin_service_app', self.test_service.id)
        self.assertEquals(resolve(url).func, update_admin_subService)

    def test_delete_admin_service_app_urls_resolves(self):
        url = url_with_args('delete_admin_service_app', self.test_service.id)
        self.assertEquals(resolve(url).func, delete_admin_subService)

    def test_apps_by_type_urls_resolves(self):
        url = reverse('apps-by-type')
        self.assertEquals(resolve(url).func, apps_by_type)

    def test_type_dashboard_urls_resolves(self):
        url = url_with_args('type-dashboard', self.test_service.id)
        self.assertEquals(resolve(url).func, type_dashboard)

    def test_delete_type_dashboard_urls_resolves(self):
        url = url_with_args('delete-type-dashboard', self.test_service.id)
        self.assertEquals(resolve(url).func, delete_type_dashboard)

    def test_update_type_dashboard_urls_resolves(self):
        url = reverse('update-type-dashboard', args=[self.test_service.id, 1])  # Replace 1 with any integer value for app_id
        self.assertEquals(resolve(url).func, update_type_dashboard)

    def test_clients_table_urls_resolves(self):
        url = reverse('clients-table')
        self.assertEquals(resolve(url).func, clients_table)

    def test_subservice_type_dashboard_urls_resolves(self):
        url = reverse('subservice-type-dashboard')
        self.assertEquals(resolve(url).func, subservice_type_dashboard)

    def test_update_subservice_type_urls_resolves(self):
        url = url_with_args('update-subservice-type', self.test_service.id)
        self.assertEquals(resolve(url).func, update_subservice_type)

    def test_delete_subservice_type_urls_resolves(self):
        url = url_with_args('delete-subservice-type', self.test_service.id)
        self.assertEquals(resolve(url).func, delete_subservice_type)