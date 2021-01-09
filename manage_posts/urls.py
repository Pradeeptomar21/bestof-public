# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Manage Posts function.
urlpatterns = [

    # Url for Manage Posts Function.
    path('', views.ManagePostsView.as_view(), name="ManagePostsView"),
    path('post-status', views.PostStatusView.as_view(), name="PostStatusView"),


    path('view-post-detail', views.PostDetailView.as_view(), name="PostDetailView"),

# path('edit/<str:id>', views.EditFoodCategoryView.as_view(), name="EditFoodCategoryView"),


]