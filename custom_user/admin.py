# Import Python Package Start
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy
# Import Developer Package Start
from .models import User


@admin.register(User) # Register User model created by developer
#  Function for Display Model into superuser page
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (ugettext_lazy('Personal info'), {'fields': ('full_name', 'user_image', 'about_me')}),
        (ugettext_lazy('Address info'), {'fields': ('address', 'location', 'zip_code', 'latitude', 'longitude', 'distance')}),
        (ugettext_lazy('Device info'), {'fields': ('device_token', 'otp')}),
        (ugettext_lazy('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (ugettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (ugettext_lazy('Update info'), {'fields': ('update_by', 'update_dt')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'is_staff')  # display field for admin
    search_fields = ('email', 'full_name')  # search field for admin
    ordering = ('date_joined',)  # table order order admin