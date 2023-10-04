from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import (
    register, login, logout, client_dashboard, activate, forgotPassword, resetpassword_validate, resetPassword
)

from accounts.models import Account

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def validate_url(name, uidb64, token):
    return reverse(name, args=[uidb64, token])

class TestUrls(TestCase):

    def setUp(self):
        self.user1 = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )


    def test_register_urls_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_login_urls_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_urls_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_client_dashboard_urls_resolves(self):
        url = reverse('client_dashboard')
        self.assertEquals(resolve(url).func, client_dashboard)

    def test_activate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('activate', uidb64, token)
        self.assertEquals(resolve(url).func, activate)

    def test_forgotPassword_urls_resolves(self):
        url = reverse('forgotPassword')
        self.assertEquals(resolve(url).func, forgotPassword)

    def test_resetpassword_validate_urls_resolves(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        url = validate_url('resetpassword_validate', uidb64, token)
        self.assertEquals(resolve(url).func, resetpassword_validate)

    def test_resetPassword_urls_resolves(self):
        url = reverse('resetPassword')
        self.assertEquals(resolve(url).func, resetPassword)


    # def test_add_urls_resolves(self):
    #     url = reverse('add')
    #     # print(resolve(url))
    #     self.assertEquals(resolve(url).func.view_class, ProjectCreateView)

    # def test_detail_urls_resolves(self):
    #     url = reverse('detail', args=['some-slug'])
    #     # print(resolve(url))
    #     self.assertEquals(resolve(url).func, project_detail)
