from django.shortcuts import render,HttpResponse,HttpResponseRedirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Delivery_Partner
from .forms import DeliveryPartnerForm
from datetime import datetime
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.

@method_decorator(login_required, name="dispatch")
class ManageDeliveryView(generic.TemplateView):
    template_name = 'bestof-admin/manage-delivery/index.html'
    delivery_partner_form = DeliveryPartnerForm

    def get(self, request, *args, **kwargs):
        delivery_partner_data = Delivery_Partner.objects.all().order_by('-id')
        return render(request, self.template_name,
                      {'delivery_partner_form':self.delivery_partner_form,'delivery_partner_data':delivery_partner_data})

    def post(self, request, *args, **kwargs):
        delivery_partner_form = DeliveryPartnerForm(request.POST)
        if delivery_partner_form.is_valid():
            # delivery_partner_form.save()
            data = delivery_partner_form.save(commit=False)
            data.created_by = request.user
            data.save()

            return HttpResponseRedirect(reverse('manage_delivery_partner_link:ManageDeliveryView'))
        # return render(request, self.template_name,
        #               {'delivery_partner_form':self.delivery_partner_form})


@method_decorator(login_required, name="dispatch")
class EditLogoDeliveryView(generic.TemplateView):
    template_name = 'bestof-admin/manage-delivery/edit-logo.html'
    delivery_partner_form = DeliveryPartnerForm

    def get(self, request, id, *args, **kwargs):
        delivery_partner_data = Delivery_Partner.objects.all().order_by('-id')
        delivery_instance = get_object_or_404(Delivery_Partner, id=id)
        # delivery_partner_form = DeliveryPartnerForm(instance=delivery_instance)

        return render(request, self.template_name,
                      {'delivery_partner_data1':delivery_instance, 'delivery_partner_data':delivery_partner_data})


@method_decorator(login_required, name="dispatch")
class EditDeliveryView(generic.TemplateView):
    template_name = 'bestof-admin/manage-delivery/edit.html'
    delivery_partner_form = DeliveryPartnerForm

    def get(self, request, id, *args, **kwargs):
        delivery_instance = get_object_or_404(Delivery_Partner, id=id)
        delivery_partner_form = DeliveryPartnerForm(instance=delivery_instance)

        return render(request, self.template_name,
                      {'delivery_partner_form':delivery_partner_form,'delivery_partner_data':delivery_instance})

    def post(self, request,id, *args, **kwargs):
        delivery_instance = get_object_or_404(Delivery_Partner, id=id)
        delivery_partner_form = DeliveryPartnerForm(request.POST, instance=delivery_instance)
        if delivery_partner_form.is_valid():
            # delivery_partner_form.save()
            data = delivery_partner_form.save(commit=False)
            data.created_by = request.user
            data.save()
    #
            return HttpResponseRedirect(reverse('manage_delivery_partner_link:ManageDeliveryView'))
    #     # return render(request, self.template_name,
    #     #               {'delivery_partner_form':self.delivery_partner_form})


@csrf_exempt
def crop_image(request):
    if True:
        check_map = request.POST['image']
        today = datetime.now()
        val = today.strftime("_%d_%m_%Y_%H_%M_%S_%f")

        format, imgstr = check_map.split(';base64,')
        ext = format.split('/')[-1]
        file_name = str(val) + "." + ext

        data = ContentFile(base64.b64decode(imgstr), name=file_name)
        id = 0
        if 'partner-id' in request.GET:
            id = request.GET['partner-id']

        # get_object = get_object_or_404(UserRegistration, pk=request.session['user_id'])
        delivery_instance = get_object_or_404(Delivery_Partner, id=id)
        if delivery_instance.logo:
            delivery_instance.logo.delete(save=False)
        delivery_instance.logo = data
        delivery_instance.save()
        return JsonResponse({'data': file_name})


@method_decorator(login_required, name="dispatch")
class DeliveryPartnerDeleteView(generic.TemplateView):
    template_name = 'bestof-admin/manage-delivery'

    def post(self, request, *args, **kwargs):
        get_id = request.POST["id_log"]
        if get_id:
            if Delivery_Partner.objects.filter(id=get_id).exists():
                Delivery_Partner.objects.filter(id=get_id).delete()
        return HttpResponseRedirect(reverse('manage_delivery_partner_link:ManageDeliveryView'))


@method_decorator(login_required, name="dispatch")
class DeliveryStatusView(generic.TemplateView):
    template_name = 'bestof-admin/manage-delivery/index.html'

    def post(self, request, *args, **kwargs):

        partnerstatusid = request.POST["partnerstatusid"]
        partnerstatus = request.POST["partnerstatus"]
        if partnerstatus == "True":
            status = False
        else:
            status = True
        Delivery_Partner.objects.filter(id=partnerstatusid).update(publish_status=status)
        # messages.info(request, "Status Changed successfully.")
        check_map = 1
        return JsonResponse({'partnerstatusid': check_map})
