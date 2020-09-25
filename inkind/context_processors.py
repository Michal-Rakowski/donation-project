from .forms import PasswordForm

def password_protected(request):
    """
    Passing password form across all views
    """
    context = {"password_form": PasswordForm}
    return context