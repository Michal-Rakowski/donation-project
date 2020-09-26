"""donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inkind import views
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from inkind.forms import CustomLoginForm

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing-page'),
    path('profile/', views.ProfileView.as_view(), name='user-profile'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/update/password-reset/', views.CustomPasswordChangeView.as_view(), 
                                                        name='password-reset'),
    path('donate/', views.AddDonationView.as_view(), name='add-donation'),
    path('donate/confirmation/', views.Confirmation.as_view(), name='form-confirmation'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.CustomLogin.as_view(template_name='inkind/login.html', 
                                            authentication_form=CustomLoginForm),
                                            name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ajax/load-institutions/', views.load_institutions, name='ajax_load'),
    path('ajax/change_status/', views.ajax_status_change, name='status-update'),
    path('admin/', admin.site.urls),
]