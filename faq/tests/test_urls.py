from django.test import TestCase
from django.urls import reverse, resolve
from faq.views import faq_question  # Import your FAQ views here
from faq.models import FAQCategory, FAQQuestion

def url_with_args(name, args):
    return reverse(name, args=[args])

def create_FAQCategory(
    home_note   = 'test home note',
    name = 'test name'
):
    return FAQCategory.objects.create(
        home_note = home_note,
        name = name
    )


class TestUrls(TestCase):

    def test_faq_list_url_resolves(self):
        url = reverse('faq_categories')
        self.assertEquals(resolve(url).func, faq_question)

    def test_faq_detail_url_resolves(self):
        category = create_FAQCategory()
        # url = reverse('faq_detail', args=[1])  # Replace 1 with a valid category ID
        url = url_with_args('faq_question', category.id)
        self.assertEquals(resolve(url).func, faq_question)
