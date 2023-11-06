from django.test import TestCase

from company.models import Company, CompanyOverview

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

def create_company_overview(
    company,
    business_overview = 'test business overview',
    competive_advantage = 'test competitive advantage',
    mission = 'test mission statement',
    vision = 'test vision',
    goal = 'test philosophy'
):
    return CompanyOverview.objects.create(
        company = company,
        business_overview = business_overview,
        competive_advantage = competive_advantage,
        mission = mission,
        vision = vision,
        goal = goal
    )


class TestModels(TestCase):

    def test_create_company(self):
        company_name = 'testcompany'
        email = 'test@testcompany.com'
        company = create_company()

        self.assertEquals(str(company), company_name)
        self.assertEquals(company.email, email)

    def test_create_company_overview(self):
        company_name = 'testcompany'
        business_overview = 'test business overview'
        company = create_company()
        company_overview = create_company_overview(company)

        self.assertEquals(str(company_overview), company_name)
        self.assertEquals(company_overview.business_overview, business_overview)