# Import Python Package Start
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy
from import_export.admin import ImportExportModelAdmin
# Import Developer Package Start
from .models import Category


class Category_Admin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'slug', 'publish_status', 'created_dt')


admin.site.register(Category, Category_Admin)

