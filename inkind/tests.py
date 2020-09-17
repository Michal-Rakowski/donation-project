from django.test import TestCase
from django.urls import reverse


class LandingPageTests(TestCase):
    def test_landing_page_access(self):
        """
        Verifies that landing page load properly and returns 200 ok status
        """
        url = reverse('landing-page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """
        Verifies whether context data are passed to the view correctly
        """
        ...


class RegisterViewTests(TestCase):
    def test_register_view_access(self):
        """
        Verifies register view is returning 200 ok status
        """
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class LoginViewTests(TestCase):
    def test_login_view_acccess(self):
        """
        Verifies login view is returning 200 ok status
        """
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AddDonationViewTests(TestCase):
    def test_add_donation_access(self):
        """
        Verifies add-donation view is accessible upon request
        """
        url = reverse('add-donation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)