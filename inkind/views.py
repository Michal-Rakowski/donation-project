from django.shortcuts import render
from django.views import generic
from django.db.models import Avg, Count, Min, Sum

from .models import Donation, Institution, Category
# Create your views here.

class LandingPageView(generic.TemplateView):
    """
    Displays landing page of the website
    """
    template_name = 'inkind/index.html'

    def get_context_data(self, **kwargs):
        """
        Calculates total of donated bags, total of supported institutions and 
        pass its value to the template
        """
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
        context['total_institutions'] = Donation.objects.aggregate(total_institutions=Count('institution'))['total_institutions']
        context['funds'] = Institution.objects.filter(institution_type='FUND')
        context['orgs'] = Institution.objects.filter(institution_type='OPOZ')
        context['locals'] = Institution.objects.filter(institution_type='ZLOK')
        return context

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