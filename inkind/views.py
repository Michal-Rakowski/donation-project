from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import views
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect 
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.utils import timezone

from .models import Donation, Institution, Category, CustomUser
from .forms import UserCreationForm, DonationForm, PasswordForm


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
        context['total_institutions'] = Donation.objects.aggregate(total_institutions=Count('institution', distinct=True))['total_institutions']
        return context

    def post(self, request, *args, **kwargs):
        """ 
        Handles Password Form for Editing User Profile
        """
        password_form = PasswordForm(self.request.POST)
        password = self.request.POST.get('password')
        user_password = self.request.user.password

        ##setting session for the user
        self.request.session['password_access'] = 'access'
        if check_password(password, user_password):
            return HttpResponseRedirect(reverse_lazy('profile-update', kwargs={'pk': self.request.user.pk}))
        else:
            messages.add_message(self.request, messages.ERROR, 'Niepoprawne hasło.')
            return HttpResponseRedirect(reverse_lazy('user-profile')) 


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
        for i_d in categories_id:
            cat = Category.objects.get(pk=i_d)
            self.object.categories.add(cat)
    
        return super().form_valid(form)


class Confirmation(views.TemplateView):
    """
    Displays confirmation upon successful donation-form submittion
    """
    template_name = 'inkind/form-confirmation.html'


def load_institutions(request):
    """Filtering Institutions on selected categories"""
    if request.method == 'POST':
        #getting categories string send throught AJAX call in form '1, 2, 3' etc
        category = request.POST.get('category')
        if category is not None:
            #converting to int list
            ids = list(map(int, [i for i in category.split(',')]))
            ## Get intitution entries with selected ids 
            institutions = Institution.objects.filter(categories__id__in=ids).distinct().order_by('name')

    return render(request, 'inkind/form-institutions.html', {'institutions': institutions})


class ProfileView(LoginRequiredMixin, generic.ListView):
    """
    User profile page. 
    Lists donations of the currently logged in user
    Added POST method for Ajax donation status update
    """
    template_name = 'inkind/profile.html'
    model = Donation
    context_object_name = 'donations'
    paginate_by = 7

    def get_queryset(self, *args, **kwargs):
        """
        Returns only donations of the current user
        """
        queryset = self.model.objects.filter(user=self.request.user).order_by('status', '-pick_up_date_time', 'pk')
        return queryset
    
    def post(self, request, *args, **kwargs):
        """
        Redirects to ajax function for status update 
        """         
        return ajax_status_change(request)


def ajax_status_change(request):
    """
    Changes Status of the donation to True:'(ODEBRANE)'
    """
    if request.method =='POST':
        status = request.POST.get('status', None)
        donation = Donation.objects.get(pk=status)
        donation.status = True
        donation.status_change = timezone.now().date()
        donation.save()
        return HttpResponseRedirect(reverse_lazy('user-profile'))


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
    User profile update view
    """
    template_name = 'inkind/profile_update.html'
    model = CustomUser
    fields = ['first_name', 'last_name','email']
    success_message = "Twój profil został zaktualizowany pomyślnie"
    success_url = reverse_lazy('user-profile')

    def get_context_data(self, **kwargs):
        """
        Passes change_password form to the context for display
        """
        context = super().get_context_data(**kwargs)
        context['change_password'] = PasswordChangeForm(user=self.request.user)
        return context

    def get_queryset(self):
        """
        User is able to access only his update page. Raises 'Page not found' for any other users
        """
        queryset = self.model.objects.filter(id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        """ 
        Checks for session and instantiate a blank version of the form.
        Redirects to profile page if session not found
        """
        self.object = self.get_object()
        ##checking if set session exists 
        if 'password_access' in self.request.session:
            #deleting session if it was there and allowing access to edit profile page
            del self.request.session['password_access']
            return self.render_to_response(self.get_context_data())
        else:
            #if the session isnt there redirecting user to their profile with message 
            messages.add_message(self.request, messages.ERROR, 'Aby zmienic ustawienia konta wybierz opcję "Ustawienia" w panelu użykownika')
            return HttpResponseRedirect(reverse_lazy('user-profile'))


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    """
    Subclasses django built-in PasswordChangeView. Gets displayed if 
    Overriding get for the access to the page
    using request.session
    Displays success message on successful form submittion 
    """

    template_name = 'inkind/password_change.html'
    success_url = reverse_lazy('user-profile')
    success_message = 'Hasło zostało zmieniono pomyślnie'

    def get(self, request, *args, **kwargs):

        """ 
        Checks for session and instantiate a blank version of the form.
        Redirects to profile page if session not found
        """
     
        if 'password_access' in self.request.session:
            del self.request.session['password_access']
            return self.render_to_response(self.get_context_data())
        else:
            messages.add_message(self.request, messages.ERROR, 'Aby zmienic ustawienia konta wybierz opcję "Ustawienia" w panelu użykownika')
            return HttpResponseRedirect(reverse_lazy('user-profile'))

