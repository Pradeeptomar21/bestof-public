from django.shortcuts import render, HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from admin_log_data.models import admin_add_log


# Create your views here.

@method_decorator(login_required, name="dispatch")
class PostCreationView(generic.TemplateView):
    template_name = 'bestof-admin/post-creations/index.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,
                      {})


