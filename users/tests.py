from django.test import TestCase

from users.forms import RegisterForm, LoginForm, CustomPasswordChangeForm
from users.models import User


# Create your tests here.
class RegisterFormTests(TestCase):
    def test__valid_register_form(self):
        form_data = {
            'username': 'test',
            'email': 'test@test.com',
            'profile_pic': 'http://test.com/avatar.png',
            'password1': 'Password1234!',
            'password2': 'Password1234!',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test__invalid_register_form_password_mismatch(self):
        form_data = {
            'username': 'test',
            'email': 'test@test.com',
            'profile_pic': 'http://test.com/avatar.png',
            'password1': 'Password1234!',
            'password2': 'differentpassword',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class LoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')

    def test__valid_login_form(self):
        form = LoginForm(data={'username': 'test', 'password': '1234'})
        self.assertTrue(form.is_valid())

    def test__invalid_login_form(self):
        form = LoginForm(data={'username': 'test', 'password': 'wrongpass'})
        self.assertFalse(form.is_valid())


class CustomPasswordChangeFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')

    def test__password_change_valid(self):
        form = CustomPasswordChangeForm(user=self.user, data={
            'old_password': '1234',
            'new_password1': 'Newpass123!',
            'new_password2': 'Newpass123!'
        })
        self.assertTrue(form.is_valid())

    def test__password_change_invalid_mismatch(self):
        form = CustomPasswordChangeForm(user=self.user, data={
            'old_password': '1234',
            'new_password1': 'Newpass123!',
            'new_password2': 'Mismatch123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)