from django.test import TestCase
from django.urls import reverse, resolve
from faq.views import (faq_list, faq_detail)  # Import your FAQ views here

class TestUrls(TestCase):

    def test_faq_list_url_resolves(self):
        url = reverse('faq_list')
        self.assertEquals(resolve(url).func, faq_list)

    def test_faq_detail_url_resolves(self):
        url = reverse('faq_detail', args=[1])  # Replace 1 with a valid category ID
        self.assertEquals(resolve(url).func, faq_detail)
