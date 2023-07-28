from django.test import TestCase
from django.shortcuts import reverse


class PagesTest(TestCase):
    def test_home_page_by_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_details(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Home Page')

    def test_about_us_page_by_url(self):
        response = self.client.get('/aboutus/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_details(self):
        response = self.client.get(reverse('aboutus'))
        self.assertContains(response, 'About Us')
