"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.hashers import make_password

from core.models import User
from core.forms import UserCreationForm
from rebar.testing import flatten_to_dict 


class UserTestCase(TestCase):
    def test_manager(self):
        email = "email@email.com"
        pw = "abcd"
        first_name = "John"
        last_name = "Doe"
        user = User.objects.create_user(email, pw,
                                        first_name=first_name,
                                        last_name=last_name)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(pw))

    def test_createsuperuser(self):
        email = "email@email.com"
        pw = "abcd"
        user = User.objects.create_user(email, pw)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(pw))

class UserCreationFormTest(TestCase):
    def test_mismatch_passwords_is_invalid(self):
        form_data = flatten_to_dict(UserCreationForm)
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['password1'] = 'abcde'
        form_data['password2'] = 'abcdef'

        bound_form = UserCreationForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

    def test_mismatch_passwords_is_invalid(self):
        form_data = flatten_to_dict(UserCreationForm)
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['password1'] = 'abcde'
        form_data['password2'] = 'abcde'

        bound_form = UserCreationForm(data=form_data)
        self.assertTrue(bound_form.is_valid())

    def test_too_short_password_is_invalid(self):
        form_data = flatten_to_dict(UserCreationForm)
        form_data['first_name'] = 'Foo'
        form_data['last_name'] = 'Bar'
        form_data['email'] = 'foo@example.com'
        form_data['password1'] = 'abcd'
        form_data['password2'] = 'abcd'

        bound_form = UserCreationForm(data=form_data)
        self.assertFalse(bound_form.is_valid())

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
