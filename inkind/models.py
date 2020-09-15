from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

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
        choices=InstitutionType.choices, default=InstitutionType.FUNDACJA)
    name = models.CharField(max_length=250)
    description = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
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
        return f'{self.user.username}({self.city}) Donation'

