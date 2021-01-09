# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views


# Define urls for User Update Application function.
urlpatterns = [

    # Url for user Update Password Function.
    path('password-otp', views.UpdatePasswordOtpView.as_view(), name="update_password_otp"),
    path('password-otp/', views.UpdatePasswordOtpView.as_view(), name="update_password_otp"),

    # Url for user Update Password Function.
    # path('password-otp-check', views.UpdatePasswordOtpCheckView.as_view(), name="update_password_otp_check"),
    # path('password-otp-check/', views.UpdatePasswordOtpCheckView.as_view(), name="update_password_otp_check"),

    # Url for user Update Password Function.
    path('password', views.UpdatePasswordView.as_view(), name="update_password"),
    path('password/', views.UpdatePasswordView.as_view(), name="update_password"),

    # Url for user Update Profile Function.
    path('profile', views.UpdateProfileView.as_view(), name="update_profile"),
    path('profile/', views.UpdateProfileView.as_view(), name="update_profile"),

    # Url for user Update Profile Function.
    path('get_profile_data', views.GetProfileDataView.as_view(), name="get_profile_data"),
    path('get_profile_data/', views.GetProfileDataView.as_view(), name="get_profile_data"),

]