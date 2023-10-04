from django.test import TestCase
from django.urls import reverse, resolve
from enquiry.views import contact_us, subscribe


class TestUrls(TestCase):

    def test_contact_us_urls_resolves(self):
        url = reverse('contact_us')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, contact_us)

    def test_subscribe_urls_resolves(self):
        url = reverse('subscribe')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, subscribe)