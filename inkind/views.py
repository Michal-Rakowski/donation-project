from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import views
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponseRedirect 
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

class CustomLogin(views.LoginView):
    """
    Subclasses Django built-in LoginView overriding POST with redirect to registration view 
    if user does not exist, redisplays login form otherwise
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            email = form.cleaned_data.get('username')
            if not email in CustomUser.objects.values_list('email', flat=True):
                return HttpResponseRedirect(reverse_lazy('register'))
            else:
                return self.form_invalid(form)
            