# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for User Application function.
urlpatterns = [

    # Url for user Registration Function.
    path('registration', views.UserRegistrationView.as_view(), name="user_registration"),
    path('registration/', views.UserRegistrationView.as_view(), name="user_registration"),

    # Url for user Login Function.
    path('login', views.UserLoginView.as_view(), name="user_login"),
    path('login/', views.UserLoginView.as_view(), name="user_login"),

    # Url for user Activate Function.
    path('activate', views.UserActivateView.as_view(), name="user_activate"),
    path('activate/', views.UserActivateView.as_view(), name="user_activate"),

]