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
        
