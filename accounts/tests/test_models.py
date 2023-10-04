"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase

from accounts.models import Account


def create_user(first_name='first', last_name='last', email='user@example.com',username='username', password='testpass123'):
    """create and return a new user."""
    return Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)


class TestsModels(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'user@example.com'
        password = 'testpass123'
        user = create_user()

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        no = 0
        for email, expected in sample_emails:
            no += 1
            username='username'+str(no)
            user = create_user(email=email, username=username)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = Account.objects.create_superuser(
            'first',
            'last',
            'username',
            'user@example.com',
            'testpass123'
        )

        self.assertTrue(user.is_superadmin)
        self.assertTrue(user.is_staff)

    # def test_create_recipe(self):
    #     """Test creating a recipe is successful."""
    #     user = get_user_model().objects.create_user(
    #         'test@examble.com',
    #         'testpass123',
    #     )
    #     recipe = models.Recipe.objects.create(
    #         user=user,
    #         title='Sample recipe name',
    #         time_minutes=5,
    #         price=Decimal('5.50'),
    #         description='Sample recipe description'
    #     )

    #     self.assertEqual(str(recipe), recipe.title)

    # def test_create_tag(self):
    #     """Test creating a tag is successful."""
    #     user = create_user()
    #     tag = models.Tag.objects.create(user=user, name='Tag1')

    #     self.assertEqual(str(tag), tag.name)

