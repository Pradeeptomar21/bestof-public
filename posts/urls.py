# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views


# Define urls for Posts Application function.
urlpatterns = [

    # Url for get posts function.
    path('', views.GetPostInfoView.as_view(), name="get_post_info"),

    # Url for get posts function.
    path('self-info', views.SelfPostInfoView.as_view(), name="self_post_info"),
    path('self-info/', views.SelfPostInfoView.as_view(), name="self_post_info"),

    # Url for get posts function.
    path('business-info', views.BusinessPostInfoView.as_view(), name="business_post_info"),
    path('business-info/', views.BusinessPostInfoView.as_view(), name="business_post_info"),


]