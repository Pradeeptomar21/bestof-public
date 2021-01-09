# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Post Creation function.
urlpatterns = [

    # Url for Post Creation Function.
    path('', views.PostCreationView.as_view(), name="PostCreationView"),


]