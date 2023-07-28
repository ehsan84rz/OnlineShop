from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class AccountsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='pass1#$Hi#Iamhere',
        )

    def test_sign_up_page_by_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_sign_up_page_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_sign_up_details(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign Up')

    def test_sign_up_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password1': 'I$Was%Here123',
            'password2': 'I$Was%Here123'
        })
        self.assertEqual(get_user_model().objects.all().count(), 2)
        self.assertEqual(get_user_model().objects.last().username, 'user2')
        self.assertEqual(get_user_model().objects.last().email, 'user2@gmail.com')

    def test_login_page_by_url(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_details(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Login')

    def test_login_form(self):
        response = self.client.post(reverse('login'), data={
            'username': 'user1',
            'password': 'pass1#$Hi#Iamhere',
        }, follow=True)
        self.assertRedirects(response, reverse('home'))
