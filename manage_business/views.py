from django.shortcuts import render,HttpResponse,HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from business_detail.models import Business_Details
from .forms import BusinessDeliveryPartnerForm
# from admin_log_data.models import admin_add_log


# Create your views here.

@method_decorator(login_required, name="dispatch")
class ManageBusinessView(generic.TemplateView):
    template_name = 'bestof-admin/manage-business/index.html'

    def get(self, request, *args, **kwargs):
        business_data = Business_Details.objects.all().order_by('-id')

        return render(request, self.template_name,
                      {'business_data':business_data})



# @method_decorator(login_required, name="dispatch")
# class EditBusinessView(generic.TemplateView):
#     template_name = 'bestof-admin/manage-business/edit.html'
#     delivery_partner_form = BusinessDeliveryPartnerForm
#
#     def get(self, request, id, *args, **kwargs):
#         business_instance = get_object_or_404(Business_Details, id=id)
#         # delivery_partner_form = DeliveryPartnerForm(instance=delivery_instance)
#
#         return render(request, self.template_name,
#                       {'business_data':business_instance, 'delivery_partner_form':self.delivery_partner_form})
#                       # {'business_data':business_instance})


@method_decorator(login_required, name="dispatch")
class EditBusinessView(generic.TemplateView):
    template_name = 'bestof-admin/manage-business/edit.html'

    def get(self, request, id, *args, **kwargs):
        business_instance = get_object_or_404(Business_Details, id=id)
        delivery_partner_form = BusinessDeliveryPartnerForm(instance=business_instance)

        return render(request, self.template_name,
                      {'business_data':business_instance, 'delivery_partner_form':delivery_partner_form})

    def post(self, request,id, *args, **kwargs):
        business_instance = get_object_or_404(Business_Details, id=id)
        delivery_partner_form = BusinessDeliveryPartnerForm(request.POST, instance=business_instance)
        if delivery_partner_form.is_valid():
            delivery_partner_form.save(commit=False)
            delivery_partner_form.save_m2m()

        return HttpResponseRedirect(reverse('manage_business_link:ManageBusinessView'))
