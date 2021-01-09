from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from business_detail.models import Business_Details, Business_Photos
from django.conf import settings
from django.contrib import messages

# Create your views here.

@method_decorator(login_required, name="dispatch")
class AdditionPhotoView(generic.TemplateView):
    template_name = 'bestof-admin/addition-of-photo/index.html'

    def get(self, request, *args, **kwargs):
        business_data = Business_Details.objects.all().order_by('-id')

        return render(request, self.template_name,
                      {'business_data':business_data})

    def post(self, request, *args, **kwargs):
        business_id = request.POST['business_id']

        photo = request.FILES.getlist('upload_images[]')

        business_instance = get_object_or_404(Business_Details, id=business_id)

        print(business_id)
        print(len(photo))


        x = len(photo)
        for i in range(1, int(x) + 1):
            photos_info = Business_Photos(business_image=photo[i - 1],
                                          Business_id=business_instance
                                          )
            photos_info.save()

            Business_Photos.objects.filter(id=photos_info.id).update(url=settings.IMAGE_BASE_URL + photos_info.business_image.url)

            print("done")

        #
        # business_data = Business_Details.objects.all().order_by('-id')

        return HttpResponseRedirect(reverse('addition_photo_link:AdditionPhotoView'))


@method_decorator(login_required, name="dispatch")
class ViewMorePhotoView(generic.TemplateView):
    template_name = 'bestof-admin/addition-of-photo/view-more-photo.html'

    def get(self, request, id, *args, **kwargs):
        business_instance = get_object_or_404(Business_Details, id=id)
        photo_data = Business_Photos.objects.filter(Business_id=business_instance).order_by('-id')
        return render(request, self.template_name,
                      {"photo_data":photo_data, "business_instance":business_instance})


@method_decorator(login_required, name="dispatch")
class SetAsDefaultView(generic.TemplateView):
    template_name = 'bestof-admin/addition-of-photo/view-more-photo.html'

    def get(self, request, id, *args, **kwargs):

        photo_instance = get_object_or_404(Business_Photos, id=id)

        Business_Photos.objects.filter(Business_id=photo_instance.Business_id).filter(set_as_default=True).update(set_as_default=False)

        Business_Photos.objects.filter(id=id).update(set_as_default=True)
        messages.info(request, "Default photo changed.")

        return render(request, self.template_name,
                      {})
