# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Manage Business View function.
urlpatterns = [

    # Url for Manage Business View Function.
    path('', views.ManageBusinessView.as_view(), name="ManageBusinessView"),

    path('edit/<str:id>', views.EditBusinessView.as_view(), name="EditBusinessView"),


]