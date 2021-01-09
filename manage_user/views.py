from django.contrib import messages

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from admin_log_data.models import admin_add_log


# Create your views here.
from custom_user.models import User


@method_decorator(login_required, name="dispatch")
class ManageUserView(generic.TemplateView):
    template_name = 'bestof-admin/manage-app-user/index.html'

    def get(self, request, *args, **kwargs):
        User_data = User.objects.all().order_by('-id')
        return render(request, self.template_name, {'User_data': User_data})

# @method_decorator(login_required, name="dispatch")
# class EditManageUserView(generic.TemplateView):
#     template_name = 'bestof-admin/manage-app-user/edit.html'
#
#     def get(self, request, id, *args, **kwargs):
#         user_instance = get_object_or_404(User, id=id)
#
#         return render(request, self.template_name,
#                       {'user_data': user_instance})
@method_decorator(login_required, name="dispatch")
class UserStatusView(generic.TemplateView):
    template_name = 'bestof-admin/manage-app-user/index.html'

    def post(self, request, *args, **kwargs):

        userstatusid = request.POST["userstatusid"]
        userstatus = request.POST["userstatus"]
        print(userstatusid)
        print(userstatus)
        if userstatus == "True":
            status = False
        else:
            status = True
        User.objects.filter(id=userstatusid).update(is_active=status)
        # messages.info(request, "Status Changed successfully.")
        check_map = 1
        return JsonResponse({'userstatusid': check_map})