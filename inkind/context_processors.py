from .forms import PasswordForm, ContactForm

def password_protected(request):
    """
    Passing password form across all views
    """
    context = {"password_form": PasswordForm,
              "contact_form": ContactForm }
    return context