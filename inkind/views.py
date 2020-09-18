from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Avg, Count, Min, Sum
from django.contrib.messages.views import SuccessMessageMixin

from .models import Donation, Institution, Category, CustomUser
from .forms import UserCreationForm
# Create your views here.

class LandingPageView(generic.ListView):
    """
    Displays landing page of the website
    """
    model = Institution
    template_name = 'inkind/index.html'
    context_object_name = 'institutions'
    #paginate_by = 5


    def get_context_data(self, **kwargs):
        """
        Calculates total of donated bags, total of supported institutions and all institution
        passes its value to the template
        """
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
        context['total_institutions'] = Donation.objects.aggregate(total_institutions=Count('institution'))['total_institutions']
        return context


class AddDonationView(generic.TemplateView):
    """
    Displays form for submitting a donation
    """
    template_name = 'inkind/form.html'


class RegistrationView(SuccessMessageMixin, generic.CreateView):
    """
    Creates user and redirects to login upon success
    """
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'inkind/register.html'
    success_url = reverse_lazy('login')
    success_message = "User was created successfully"