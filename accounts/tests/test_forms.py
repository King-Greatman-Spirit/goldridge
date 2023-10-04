from django.test import TestCase
from accounts.forms import RegistrationForm


class TestForms(TestCase):

    def test_registration_form_valid_data(self):
        form = RegistrationForm(data={
            'first_name': 'first',
            'last_name': 'last',
            'phone_number': '11122233344',
            'email': 'user1@example.com',
            'username': 'first_last',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })

        self.assertTrue(form.is_valid())

    def test_registration_form_no_data(self):
        form = RegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)