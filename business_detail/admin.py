# Import Python Package Start
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Import Developer Package Start
from .models import Business_Details, Business_categories, Business_Photos, Business_Time, Business_Posts, Post_Activity, Remove_Activity


class Business_Details_Admin(ImportExportModelAdmin):
    search_fields = ['name', 'business_id']
    list_display = ('name', 'business_id', 'business_display_address', 'zip_code')


class Business_categories_Admin(ImportExportModelAdmin):
    search_fields = ['title']
    list_display = ('Business_id', 'title', 'publish_status')


class Business_Photos_Admin(ImportExportModelAdmin):
    list_display = ('Business_id', 'url')

class Business_Time_Admin(ImportExportModelAdmin):
    list_display = ('Business_id','is_overnight', 'start','end')


admin.site.register(Business_Details, Business_Details_Admin)
admin.site.register(Business_categories, Business_categories_Admin)
admin.site.register(Business_Photos, Business_Photos_Admin)
admin.site.register(Business_Time, Business_Time_Admin)
admin.site.register(Business_Posts)
admin.site.register(Remove_Activity)
admin.site.register(Post_Activity)


