from django.test import TestCase
from django.urls import reverse, resolve
from company.views import (
   company, company_dashboard, update_company, delete_company,
   business_overview, update_business_overview, delete_business_overview
)

from company.models import Company, CompanyOverview
from accounts.models import Account

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
        self.test_company_overview = CompanyOverview.objects.create(
            company = self.test_company,
            business_overview = 'test business overview',
            competive_advantage = 'test competitive advantage',
            mission = 'test mission statement',
            vision = 'test vision',
            goal = 'test philosophy'
        )

    def test_company_urls_resolves(self):
        url = reverse('company')
        self.assertEquals(resolve(url).func, company)

    def test_company_dashboard_urls_resolves(self):
        url = reverse('company_dashboard')
        self.assertEquals(resolve(url).func, company_dashboard)

    def test_update_company_urls_resolves(self):
        url = url_with_args('update_company', self.test_company.id)
        self.assertEquals(resolve(url).func, update_company)

    def test_delete_company_urls_resolves(self):
        url = url_with_args('delete_company', self.test_company.id)
        self.assertEquals(resolve(url).func, delete_company)

    def test_business_overview_urls_resolves(self):
        url = reverse('business_overview')
        self.assertEquals(resolve(url).func, business_overview)

    def test_update_business_overview_urls_resolves(self):
        url = url_with_args('update_business_overview', self.test_company_overview.id)
        self.assertEquals(resolve(url).func, update_business_overview)

    def test_delete_business_overview_urls_resolves(self):
        url = url_with_args('delete_business_overview', self.test_company_overview.id)
        self.assertEquals(resolve(url).func, delete_business_overview)

    # def test_resetPassword_urls_resolves(self):
    #     url = reverse('resetPassword')
    #     self.assertEquals(resolve(url).func, resetPassword)


    # # def test_add_urls_resolves(self):
    # #     url = reverse('add')
    # #     # print(resolve(url))
    # #     self.assertEquals(resolve(url).func.view_class, ProjectCreateView)

    # # def test_detail_urls_resolves(self):
    # #     url = reverse('detail', args=['some-slug'])
    # #     # print(resolve(url))
    # #     self.assertEquals(resolve(url).func, project_detail)
