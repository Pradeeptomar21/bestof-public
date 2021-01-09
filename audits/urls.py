# Import some useful packages.
from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from . import views

# Define urls for Audits function.
urlpatterns = [

    # Url for Audits Function.
    path('', views.AuditView.as_view(), name="AuditView"),
    path('audit-detail', views.AuditDetailView.as_view(), name="AuditDetailView"),

    path('vote-up', views.VoteUpView.as_view(), name="VoteUpView"),
    path('vote-down', views.VoteDownView.as_view(), name="VoteDownView"),
    path('category-detail', views.CategoryDetailView.as_view(), name="CategoryDetailView"),

    path('like-up', views.LikeUpView.as_view(), name="LikeUpView"),
    path('like-down', views.LikeDownView.as_view(), name="LikeDownView"),

    path('post-detail', views.PostDetailView.as_view(), name="PostDetailView"),

    path('user-detail', views.UserDetailView.as_view(), name="UserDetailView"),
    path('keyword-detail', views.KeywordDetailView.as_view(), name="KeywordDetailView"),


]