# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for User Application function.
urlpatterns = [

    # Url for user Registration Function.
    path('', views.CategoryView.as_view(), name="category_view"),

]