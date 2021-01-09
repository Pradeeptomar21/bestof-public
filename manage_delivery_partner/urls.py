# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Manage Business View function.
urlpatterns = [

    # Url for Manage Business View Function.
    path('', views.ManageDeliveryView.as_view(), name="ManageDeliveryView"),

    path('edit/<str:id>', views.EditDeliveryView.as_view(), name="EditDeliveryView"),
    path('edit-logo/<str:id>', views.EditLogoDeliveryView.as_view(), name="EditLogoDeliveryView"),

    path('crop-image', views.crop_image, name='crop_image'),
    path('crop-image/', views.crop_image, name='crop_image'),

    path('delete', views.DeliveryPartnerDeleteView.as_view(), name="DeliveryPartnerDeleteView"),

    path('delivery-status', views.DeliveryStatusView.as_view(), name="DeliveryStatusView"),

]