"""BestOfProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # add package for reset admin password

urlpatterns = [
    path('superadmin/', admin.site.urls),  # admin or superadmin url link
    # admin reset password link
    path('superadmin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
    path('superadmin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),

    path('admin/login/', auth_views.LoginView.as_view(template_name='bestof-admin/login/index.html'),name="admin_login"),
    path('logout', auth_views.LogoutView.as_view() ,name="logout"),

    # urls for API
    path('api/user/', include(('user_app.urls','user_app'),namespace='user_app_link')),

    path('api/update/', include(('update_detail.urls','update_detail'),namespace='update_detail_app_link')),

    path('api/business/', include(('business_detail.urls','business_detail'),namespace='business_detail_app_link')),

    path('api/posts/', include(('posts.urls','posts'),namespace='posts_app_link')),

    path('api/notification/', include(('notification.urls','notification'),namespace='notification_app_link')),

    path('api/category', include(('category_app.urls','category_app'),namespace='category_app_link')),
    path('api/category/', include(('category_app.urls','category_app'),namespace='category_app_link/')),

    # urls for Admin
    path('admin/', include(('audits.urls','audits'),namespace='audits_link')),
    # path('admin/', include(('audits.urls','audits'),namespace='audits_link/')),

    path('admin/manage-food-category', include(('manage_food_category.urls','manage_food_category'),namespace='manage_food_category_link')),
    path('admin/manage-food-category/', include(('manage_food_category.urls','manage_food_category'),namespace='manage_food_category_link/')),

    path('admin/voting', include(('voting.urls','voting'),namespace='voting_link')),
    path('admin/voting/', include(('voting.urls','voting'),namespace='voting_link/')),

    path('admin/addition-of-photo', include(('addition_photo.urls','addition_photo'),namespace='addition_photo_link')),
    path('admin/addition-of-photo/', include(('addition_photo.urls','addition_photo'),namespace='addition_photo_link/')),

    path('admin/post-creation', include(('post_creation.urls','post_creation'),namespace='post_creation_link')),
    path('admin/post-creation/', include(('post_creation.urls','post_creation'),namespace='post_creation_link/')),

    path('admin/manage-posts', include(('manage_posts.urls','manage_posts'),namespace='manage_posts_link')),
    path('admin/manage-posts/', include(('manage_posts.urls','manage_posts'),namespace='manage_posts_link/')),

    path('admin/manage-app-user', include(('manage_user.urls','manage_user'),namespace='manage_user_link')),
    path('admin/manage-app-user/', include(('manage_user.urls','manage_user'),namespace='manage_user_link/')),

    path('admin/manage-business', include(('manage_business.urls', 'manage_business'), namespace='manage_business_link')),
    path('admin/manage-business/', include(('manage_business.urls', 'manage_business'), namespace='manage_business_link/')),

    path('admin/manage-delivery-partner', include(('manage_delivery_partner.urls', 'manage_delivery_partner'), namespace='manage_delivery_partner_link')),
    path('admin/manage-delivery-partner/', include(('manage_delivery_partner.urls', 'manage_delivery_partner'), namespace='manage_delivery_partner_link/')),

                  path('admin/admin-setting', include(('admin_setting.urls', 'admin_setting'), namespace='admin_setting_link')),
    path('admin/admin-setting/', include(('admin_setting.urls', 'admin_setting'), namespace='admin_setting_link/')),

                  # path('admin-audits', include(('audits.urls','audits'),namespace='admin_audits_link')),
    # path('admin-audits/', include(('audits.urls','audits'),namespace='admin_audits_link')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
