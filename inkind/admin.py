from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *

class CategoryInline(admin.TabularInline):
    model = Institution.categories.through
    template = 'inkind/admin/tabular.html'

class InstitutionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'institution_type']}),
        ('Opis', {'fields': ['description']}),
        ]
    list_display = ('name', 'institution_type', 'description')
    inlines = [
        CategoryInline
    ]
    exclude = ('categories',)

class DonationInline(admin.TabularInline):
    model = Donation.categories.through
    template = 'inkind/admin/tabular.html'

class DonationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Strony darowizny',               {'fields': ['user', 'institution']}),
        ('Adress odbioru', {'fields': ['address', 'city', 'zip_code']}),
        ('Szczegóły odbioru', {'fields': ['pick_up_date_time',  'phone_number','pick_up_comment']}),
        ('Szczególy darowizny', {'fields': ['quantity']}),
        ]
    list_display = ('__str__', 'institution', 'user', 'city', 'quantity')
    inlines = [
        DonationInline
    ]
    exclude = ('categories',)
# Register your models here.
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Category)



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'first_name', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)