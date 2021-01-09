# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Manage User View function.
urlpatterns = [

    # Url for Manage User View Function.
    path('', views.ManageUserView.as_view(), name="ManageUserView"),
    # path('edit/<str:id>', views.EditManageUserView.as_view(), name="EditManageUserView"),
    path('user-status', views.UserStatusView.as_view(), name="UserStatusView"),

]