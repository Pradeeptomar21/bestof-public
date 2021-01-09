# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Addition Photo function.
urlpatterns = [

    # Url for Addition Photo Function.
    path('', views.AdditionPhotoView.as_view(), name="AdditionPhotoView"),


    path('view-more-photo/<str:id>', views.ViewMorePhotoView.as_view(), name="ViewMorePhotoView"),

    path('set-as-default/<str:id>', views.SetAsDefaultView.as_view(), name="SetAsDefaultView"),




]