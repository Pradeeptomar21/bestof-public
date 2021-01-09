# from django.shortcuts import render, HttpResponse,redirect,reverse
# from django.http import HttpResponseRedirect
# from django.views import generic
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# # from admin_log_data.models import admin_add_log
# from django.contrib import messages
#
# # Create your views here.
# from admin_setting.forms import AdminSettingForm
#
# #
# @method_decorator(login_required, name="dispatch")
# class AdminSettingView(generic.TemplateView):
#     template_name = 'bestof-admin/admin-setting/index.html'
#     form = AdminSettingForm
#     def get(self, request, *args, **kwargs):
#         form = AdminSettingForm
#         return render(request, self.template_name,
#                       {'form':form})
#
#
#
#
#
#
