from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import views
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect 
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Donation, Institution, Category, CustomUser
from .forms import UserCreationForm


class LandingPageView(generic.ListView):
    """
    Displays landing page of the website which renders list of institions, set by 'self.model`
    """
    model = Institution
    template_name = 'inkind/index.html'
    context_object_name = 'institutions'
    #paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Calculates total of donated bags, total of supported institutions and
        passes its value to the template
        """
        context = super().get_context_data(**kwargs)
        context['total_bags'] = Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags']
        context['total_institutions'] = Donation.objects.aggregate(total_institutions=Count('institution'))['total_institutions']
        return context


class RegistrationView(SuccessMessageMixin, generic.CreateView):
    """
    Creates user and redirects to login page upon success
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

from .forms import DonationForm
from .models import Donation

class AddDonationView(LoginRequiredMixin, generic.FormView):
    """
    Displays form for submitting a donation
    """
    template_name = 'inkind/form.html'
    form_class = DonationForm
    extra_context = {'categories': Category.objects.all().order_by('id')}
    success_url = reverse_lazy('form-confirmation')

    def form_valid(self, form):
        """
        Sets current user to his donation, sets institution for created donations
        and creates donation.
        Add selected categories to donation
        """
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        org = self.request.POST.get('organization')
        institution = Institution.objects.get(pk=int(org))
        self.object.institution = institution
        self.object.save()
        category = self.request.POST.getlist('category')
        categories_id = list(map(int, category))
        for pk in categories_id:
            cat = Category.objects.get(pk=pk)
            self.object.categories.add(cat)
    
        return super().form_valid(form)


class Confirmation(views.TemplateView):
    template_name = 'inkind/form-confirmation.html'



def load_institutions(request):
    """Filtering Institutions on selected categories"""
    #getting categories string
    if request.method == 'POST':
        category = request.POST.get('category')
        print(category)
        if category is not None:
            ids = list(map(int, [i for i in category.split(',')]))
            institutions = Institution.objects.filter(categories__id__in=ids).distinct().order_by('name')

    return render(request, 'inkind/form-institutions.html', {'institutions': institutions})