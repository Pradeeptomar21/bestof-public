# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for User Application function.
urlpatterns = [

    # Url for user Registration Function.
    path('', views.YelpAPIView.as_view(), name="YelpAPIView"),

    # Url for Get business information.
    path('get_info', views.BusinessGetInfoView.as_view(), name="business_get_info"),
    path('get_info/', views.BusinessGetInfoView.as_view(), name="business_get_info"),

    # Url for business information from business id if not exit then save.
    path('info', views.BusinessInfoView.as_view(), name="business_info"),
    path('info/', views.BusinessInfoView.as_view(), name="business_info"),

    # Url for business information from business id if not exit then save.
    path('search', views.BusinessSearchView.as_view(), name="business_search"),
    path('search/', views.BusinessSearchView.as_view(), name="business_search"),

    # Url for business Vote Function.
    path('vote', views.BusinessVoteView.as_view(), name="business_vote"),
    path('vote/', views.BusinessVoteView.as_view(), name="business_vote"),

    # Url for business Like Function.
    path('like', views.BusinessLikeView.as_view(), name="business_like"),
    path('like/', views.BusinessLikeView.as_view(), name="business_like"),

    # Url for business information from business id if not exit then save.
    path('search-keyword', views.SearchKeywordView.as_view(), name="search_keyword"),
    path('search-keyword/', views.SearchKeywordView.as_view(), name="search_keyword"),

]