# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Manage Food Category function.
urlpatterns = [

    # Url for Manage Food Category Function.
    path('', views.ManageFoodCategoryView.as_view(), name="ManageFoodCategoryView"),

    path('category-status', views.CategoryStatusView.as_view(), name="CategoryStatusView"),

    path('edit/<str:id>', views.EditFoodCategoryView.as_view(), name="EditFoodCategoryView"),
    path('delete', views.FoodCategoryDeleteView.as_view(), name="FoodCategoryDeleteView"),


]