from django.shortcuts import render
from django.views import generic
# Create your views here.

class LandingPageView(generic.TemplateView):
    """
    Displays landing page of the website
    """
    template_name = 'inkind/index.html'


class AddDonationView(generic.TemplateView):
    """
    Displays form for submitting a donation
    """
    template_name = 'inkind/form.html'

class LoginView(generic.TemplateView):
    """
    Displays login form
    """
    template_name = 'inkind/login.html'

class RegistrationView(generic.TemplateView):
    """
    Dispplays Registration form
    """
    template_name = 'inkind/register.html'