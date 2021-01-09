# Import some useful packages.
from django.urls import path
from django.urls import reverse_lazy

# from django.views.decorators.csrf import csrf_exempt
from . import views
from django.contrib.auth import views as auth_view
# Define urls for Admin Setting View function.
urlpatterns = [

    # Url for Admin Setting View Function.
    # path('', views.AdminSettingView.as_view(), name="AdminSettingView"),
    path('',
         auth_view.PasswordChangeView.as_view(template_name='bestof-admin/admin-setting/index.html', success_url=reverse_lazy('admin_setting_link:admin_password_change')),
         name="admin_password_change"),



]