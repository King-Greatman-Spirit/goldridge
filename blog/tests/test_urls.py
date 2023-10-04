from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import (
   article, blog, search
)

from blog.models import Article, Paragraph
from company.models import Company
from accounts.models import Account

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
        self.article = Article.objects.create(
            article_title = 'Test Title',
            article_subtitle = 'Test Subtitle',
            # image = ContentFile(self.photo_file.read(), 'test_image.png'),
            tags = 'testing, test, tagging, tags'
        )
        self.paragraph = Paragraph.objects.create(
            article = self.article,
            paragraph_title = 'paragraph title',
            paragraph_content = 'test paragraph content'
        )


    def test_blog_urls_resolves(self):
        url = reverse('blog')
        self.assertEquals(resolve(url).func, blog)

    def test_blog_by_urls_urls_resolves(self):
        url = url_with_args('blog_by_keyword', 'test')
        self.assertEquals(resolve(url).func, blog)

    def test_article_urls_resolves(self):
        url = url_with_args('article', self.article.id)
        self.assertEquals(resolve(url).func, article)

    def test_search_urls_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)


