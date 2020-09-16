from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):

    class InstitutionType(models.TextChoices):
        FUNDACJA = 'FUND', _('Fundacja')
        ORGANIZACJA_POZARZADOWA = 'OPOZ', _('Organizacja pozarządowa')
        ZBIORKA_LOCALNA = 'ZLOK', _('Zbiórka lokalna')

    institution_type = models.CharField(max_length=4, 
        choices=InstitutionType.choices, default=InstitutionType.FUNDACJA, blank=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser):
    """Custom User Model 
    Required fields: Email, First name, Last name, Password
    """
    first_name = models.CharField(_('First name'), max_length=150)
    last_name = models.CharField(_('Last name'), max_length=150)
    email = models.EmailField(_('Email address'), max_length=255, unique=True, 
        error_messages={
            'unique': _('A user with such email already exists.'),
            },
    )
    is_staff = models.BooleanField(_('Staff status'), default=False, help_text=
            _('Designates whether the user can log in into admin site.'))
    is_active = models.BooleanField(_('Active'), default=True, help_text=
            _('Designates whether this user should be treated as active.'
              'Unselect this instead of deleting accounts.'))
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, inkind):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) 
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    
    quantity = models.PositiveSmallIntegerField(verbose_name="Liczba worków")
    address = models.CharField(max_length=150, verbose_name="Ulica i numer domu")
    phone_number = models.CharField(max_length=25, verbose_name="Numer telefonu")
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=15)
    pick_up_date = models.DateField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.last_name}({self.city}) Donation'


