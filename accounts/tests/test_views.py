"""
Test for Account views
"""
import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from accounts.models import Account
from company.models import Company
from accounts.forms import RegistrationForm

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    # file.name = 'test_image.png'
    file.seek(0)
    return file

def validate_url(name, uidb64, token):
    return reverse(name, args=[uidb64, token])


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.forgotPassword_url = reverse('forgotPassword')
        self.resetPassword_url = reverse('resetPassword')
        self.client_dashboard_url = reverse('client_dashboard')

        self.admin_register_url = reverse('admin_register')
        self.admin_login_url = reverse('admin_login')
        self.admin_logout_url = reverse('admin_logout')
        self.admin_forgot_password_url = reverse('admin_forgot_password')
        self.admin_reset_password_url = reverse('admin_reset_password')
        self.admin_dashboard_url = reverse('admin_dashboard')

        self.photo_file = generate_photo_file()
        self.company = Company.objects.create(
            company_name = 'testcompany',
            website_address = 'http://testcompany.com',
            email = 'test@testcompany.com',
            address_line_1 = 'address line 1',
            city = 'test city',
            state = 'test state',
            postal_code = 'test code',
            country = 'test country',
            phone = 'testphone',
            logo = ContentFile(self.photo_file.read(), 'test_image.png')
        )
        self.user1 = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )

    def test_register_GET(self):
        res = self.client.get(self.register_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/register.html')

    def test_register_POST(self):
        res = self.client.post(self.register_url, {
            'first_name': 'first',
            'last_name': 'last',
            'email': 'user@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'phone_number': '11122233344'
        })

        self.assertEquals(res.status_code, 302)
        self.assertTrue(Account.objects.filter(email='user@example.com').exists())
        self.assertRedirects(res, '/accounts/login/?command=verification&email=user@example.com')

    def test_login_GET(self):
        res = self.client.get(self.login_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/login.html')

    def test_login_verified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals('testpass123', test_user.password)
        self.assertRedirects(res, reverse('client_dashboard'))

    def test_login_unverified_user_POST(self):
        res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals('testpass123', test_user.password)
        self.assertRedirects(res, '/accounts/login/')

    def test_login_POST_wrong_details(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        res = self.client.post(self.login_url, {
            'email' : 'user@test.com',
            'password': 'testpass12'
        })

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.login_url)

    def test_logout(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        logout_res = self.client.get(self.logout_url)

        self.assertEquals(logout_res.status_code, 302)
        self.assertRedirects(logout_res, self.login_url)

    def test_forgotPassword_GET(self):
        res = self.client.get(self.forgotPassword_url)
        # print(self.company)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/forgotPassword.html')

    def test_forgotPassword_verified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        res = self.client.post(self.forgotPassword_url, {'email' : 'user1@example.com'})

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.login_url)

    def test_forgotPassword_unverified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()
        res = self.client.post(self.forgotPassword_url, {'email' : 'user@example.com'})

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.forgotPassword_url)

    def test_activate(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)

        url = validate_url('activate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.login_url)

    def test_invalid_activation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(0))
        token = default_token_generator.make_token(test_user)

        url = validate_url('activate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.register_url)

    def test_valid_resetpassword_validation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)

        url = validate_url('resetpassword_validate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.resetPassword_url)

    def test_invalid_resetpassword_validation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(0))
        token = default_token_generator.make_token(test_user)

        url = validate_url('resetpassword_validate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.login_url)

    def test_resetPassword_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)

        url = validate_url('resetpassword_validate',uidb64, token)
        validate_res = self.client.get(url)

        res = self.client.post(self.resetPassword_url, {
            'password': 'newtestpass',
            'confirm_password': 'newtestpass'
        })

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.login_url)

    def test_client_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.client_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/client_dashboard.html')

    def test_client_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.save()

        login_res = self.client.post(self.login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        # Simulate a POST request to update user details
        res = self.client.post(self.client_dashboard_url, {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': '1234567890',
            'email': 'new_email@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        })
        # print(res.context['form'].errors)

        # Check the response status code
        self.assertEquals(res.status_code, 302)

        # Retrieve the updated User instance using the known email
        updated_user = Account.objects.get(email='new_email@example.com')

        # Check whether the User details are updated successfully
        self.assertEquals(updated_user.first_name, 'First Name')
        self.assertEquals(updated_user.last_name, 'Last Name')
        self.assertEquals(updated_user.phone_number, '1234567890')

        # Check the redirection
        self.assertRedirects(res, self.client_dashboard_url, target_status_code=302)

    def test_admin_register_GET(self):
        res = self.client.get(self.admin_register_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/admin/admin_register.html')

    def test_admin_register_POST(self):
        res = self.client.post(self.admin_register_url, {
            'first_name': 'first',
            'last_name': 'last',
            'email': 'user@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'phone_number': '11122233344'
        })

        self.assertEquals(res.status_code, 302)
        # Check if the user with email 'user@example.com' and is_admin=True exists
        admin_user = Account.objects.filter(email='user@example.com', is_admin=True).first()
        self.assertIsNotNone(admin_user, "Admin user should be created")
        self.assertTrue(admin_user.check_password('testpass123'), "Password should be set correctly")
        self.assertTrue(Account.objects.filter(email='user@example.com', is_admin=True).exists())  # Check is_admin field
        self.assertRedirects(res, '/accounts/admin_login/?command=verification&email=user@example.com')


    def test_admin_login_GET(self):
        res = self.client.get(self.admin_login_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/admin/admin_login.html')

    def test_admin_login_verified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        self.assertIn('_auth_user_id', self.client.session)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals('testpass123', test_user.password)
        self.assertRedirects(res, reverse('admin_dashboard'))

    def test_admin_login_unverified_user_POST(self):
        res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(res.status_code, 302)
        # self.assertEquals('testpass123', test_user.password)
        self.assertRedirects(res, '/accounts/admin_login/')

    def test_admin_login_POST_wrong_details(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()
        res = self.client.post(self.admin_login_url, {
            'email' : 'user@test.com',
            'password': 'testpass12'
        })

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_login_url)

    def test_admin_logout(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()
        login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        logout_res = self.client.get(self.admin_logout_url)

        self.assertEquals(logout_res.status_code, 302)
        self.assertRedirects(logout_res, self.admin_login_url)

    def test_admin_forgotpassword_GET(self):
        res = self.client.get(self.admin_forgot_password_url)
        # print(self.company)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/admin/admin_forgot_password.html')

    def test_admin_forgotpassword_verified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()
        res = self.client.post(self.admin_forgot_password_url, {'email' : 'user1@example.com'})

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_login_url)

    def test_admin_forgotpassword_unverified_user_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()
        res = self.client.post(self.admin_forgot_password_url, {'email' : 'user@example.com'})

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_forgot_password_url)

    def test_admin_activate(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        test_user.is_admin = True
        test_user.save()

        url = validate_url('admin_activate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_login_url)

    def test_invalid_admin_activation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(0))
        token = default_token_generator.make_token(test_user)
        test_user.is_admin = True
        test_user.save()

        url = validate_url('admin_activate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_register_url)

    def test_valid_admin_resetpassword_validation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        test_user.is_admin = True
        test_user.save()

        url = validate_url('admin_resetpassword_validate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_reset_password_url)

    def test_invalid_admin_resetpassword_validation(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(0))
        token = default_token_generator.make_token(test_user)
        test_user.is_admin = True
        test_user.save()

        url = validate_url('admin_resetpassword_validate',uidb64, token)
        res = self.client.get(url)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_login_url)

    def test_admin_resetPassword_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        uidb64 = urlsafe_base64_encode(force_bytes(test_user.pk))
        token = default_token_generator.make_token(test_user)
        test_user.is_admin = True
        test_user.save()

        url = validate_url('admin_resetpassword_validate',uidb64, token)
        validate_res = self.client.get(url)

        res = self.client.post(self.admin_reset_password_url, {
            'password': 'newtestpass',
            'confirm_password': 'newtestpass'
        })

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, self.admin_login_url)

    def test_admin_dashboard_GET(self):
        # Test for admin user
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.admin_dashboard_url)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, 'accounts/admin/admin_dashboard.html')

    def test_admin_dashboard_POST(self):
        # Test for admin user
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        # Simulate a POST request to update user details
        res = self.client.post(self.admin_dashboard_url, {
            'first_name': 'New First Name',
            'last_name': 'New Last Name',
            'phone_number': '1234567890',
            'email': 'new_email@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        })
        # print(res.context['form'].errors)

        # Check the response status code
        self.assertEquals(res.status_code, 302)

        # Retrieve the updated User instance
        updated_admin = Account.objects.get(email='new_email@example.com')

        # Check whether the User details are updated successfully
        self.assertEquals(updated_admin.first_name, 'New First Name')
        self.assertEquals(updated_admin.last_name, 'New Last Name')
        self.assertEquals(updated_admin.phone_number, '1234567890')

        # Check the redirection
        self.assertRedirects(res, self.admin_dashboard_url, target_status_code=302)

    def test_non_admin_user_access(self):
        # Create a client user
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='nonadmin@example.com',
            password='testpass1234',
            username='test first_last'
        )

        # Make the client user as a client, not an admin
        self.user.is_admin = False  # Set 'is_admin' to False to make the user a client
        self.user.is_active = True  # Set 'is_active' to True
        self.user.save()
        
        # Try to access the admin logout view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_logout = self.client.get(self.admin_logout_url)

        # Check that the client is redirected to the login page after attempting admin logout
        self.assertEquals(res_logout.status_code, 302)
        self.assertFalse(res_logout.url.startswith(self.admin_logout_url))  # Ensure not redirected to admin logout view

        # Try to access the admin dashboard view as a client
        res_dashboard = self.client.get(self.admin_dashboard_url)

        # Check that the client is redirected to the login page when attempting to access admin dashboard
        self.assertEquals(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.admin_dashboard_url))  # Ensure not redirected to admin dashboard view

    
def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))


