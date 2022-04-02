from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import SignUpForm


def delete_user(username: str = 'usertest'):
    user = User.objects.filter(username=username).first()
    if user:
        user.delete()


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.form_data = {
            'username': 'usertest',
            'password1': 'VpyuGkbk6GJvrXJ',
            'password2': 'VpyuGkbk6GJvrXJ'
        }

    def doCleanup(self):
        delete_user(self.form_data['username'])

    def test_registration_form(self):
        form = SignUpForm(self.form_data)
        self.assertTrue(form.is_valid(), 'Error with SignUpForm.')

    def test_registration_view(self):
        response = self.client.get('/accounts/registration/')
        self.assertEqual(response.status_code, 200,
                         "Can't get the registration page.")
        response = self.client.post('/accounts/registration/',
                                    self.form_data,
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated,
                        "Error in sending data on the registration page.")
        self.client.logout()


class LoginAndLogoutTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {'username': 'usertest', 'password': 'usertest'}
        User.objects.create_user(**self.user_data)

    def doCleanup(self):
        delete_user(self.user_data['username'])

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200,
                         "Can't get the login page.")
        response = self.client.post('/accounts/login/',
                                    self.user_data,
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated,
                        "Error in sending data on the registration page.")
        self.client.logout()

    def test_logout_view(self):
        self.client.login(**self.user_data)
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated,
                         "Can't logout.")
