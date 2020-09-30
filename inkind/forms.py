from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Donation, Institution, Category
from django.contrib.auth.password_validation import get_password_validators, validate_password

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), validators=[validate_password])
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    class Meta:
        model = CustomUser
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name' : forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email'     : forms.TextInput(attrs={'placeholder': 'E-Mail'}),
        }
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Hasło'}))

from django.utils import timezone

def pick_up_date():
    return timezone.now() + timezone.timedelta(days=1)

def pick_up_date_validator(value):
    if value < timezone.now():
        raise ValidationError("Data odbioru nie może być z przeslości")

class DonationForm(forms.ModelForm):
    """
    Form for submitting donation
    """
    quantity = forms.IntegerField(required=True, label='Liczba 60l worków: ', initial=1)
    address = forms.CharField(widget=forms.TextInput, max_length=150, required=True)
    phone_number = forms.CharField(widget=forms.TextInput, required=True)
    city = forms.CharField(widget=forms.TextInput, required=True)
    zip_code = forms.CharField(widget=forms.TextInput, required=True)
    pick_up_date_time = forms.SplitDateTimeField(
        initial=pick_up_date,
        required=True,
        widget=forms.SplitDateTimeWidget, validators=[pick_up_date_validator])
    pick_up_comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Donation
        exclude = ('user', 'categories', 'status', 'status_change')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].queryset = Institution.objects.none()


class DonationStatusForm(forms.ModelForm):
    """
    Form for users allowing to change status of the particular donation
    True: if donation has been picked up 
    False: otherwise
    """
    class Meta: 
        model = Donation
        fields = ('status',)


class PasswordForm(forms.Form):
    """
    Form for accessing user profile update view
    """
    password = forms.CharField(widget=forms.PasswordInput)   


class ContactForm(forms.Form):
    """
    Form for sending email to site-admins
    """
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'row': 1,'style': 'height: 3em;','placeholder': 'Wiadomość'}))
