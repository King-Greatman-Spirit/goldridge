from django.test import TestCase

from blog.models import Author, Article, Paragraph
from company.models import Company
from service.models import Service


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

def create_author(
    first_name = 'John',
    last_name = 'Doe',
    job_title = 'tester',
    company_name = 'test company',
    email = 'test@test.com',
    phone_number = '111222333'
):
    return Author.objects.create(
        first_name = first_name,
        last_name = last_name,
        job_title = job_title,
        company_name = company_name,
        email = email,
        phone_number = phone_number
    )

def create_article(
    article_title = 'Test Title',
    article_subtitle = 'Test Subtitle'
):
    return Article.objects.create(
        article_title = article_title,
        article_subtitle = article_subtitle
    )

def create_paragraph(
    article,
    paragraph_title = 'paragraph title',
    paragraph_content = 'test paragraph content'
):
    return Paragraph.objects.create(
        article = article,
        paragraph_title = paragraph_title,
        paragraph_content = paragraph_content
    )


class TestModels(TestCase):

    def test_create_author(self):
        first_name = 'John'
        email = 'test@test.com'
        author = create_author()

        self.assertEquals(str(author), first_name)
        self.assertEquals(author.email, email)

    def test_create_article(self):
        article_title = 'Test Title'
        article_subtitle = 'Test Subtitle'
        author = create_author()
        company = create_company()
        service = create_service(company)
        article = create_article()
        article.article_author.add(author)
        article.article_service.add(service)

        self.assertEquals(str(article), article_title)
        self.assertEquals(article.article_subtitle, article_subtitle)
        self.assertIn(author, article.article_author.all())
        self.assertIn(service, article.article_service.all())

    def test_create_paragraph(self):
        paragraph_title = 'paragraph title'
        paragraph_content = 'test paragraph content'
        article = create_article()
        paragraph = create_paragraph(article)

        self.assertEquals(str(paragraph), paragraph_title)
        self.assertEquals(paragraph.paragraph_content, paragraph_content)



