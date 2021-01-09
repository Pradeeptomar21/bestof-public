# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Voting function.
urlpatterns = [

    # Url for Voting Function.
    path('', views.VotingView.as_view(), name="VotingView"),
    path('voting_details/<str:id>', views.Voting_Details.as_view(), name="Voting_Details"),

]