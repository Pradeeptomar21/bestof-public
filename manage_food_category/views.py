from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from category_app.models import Category
from django.contrib import messages

# Create your views here.
from manage_food_category.forms import FoodCategoryForm


@method_decorator(login_required, name="dispatch")
class ManageFoodCategoryView(generic.TemplateView):
    template_name = 'bestof-admin/manage-food-category/index.html'

    def get(self, request, *args, **kwargs):
        category_data = Category.objects.all()

        return render(request, self.template_name,
                      {"category_data": category_data})

    def post(self, request, *args, **kwargs):
        Category_name = request.POST["Category_name"]
        name = Category_name.lower()
        if Category.objects.filter(name=name).exists():
            messages.error(request, "This category already exists.")
        else:
            data = Category(name=name)
            data.save()
            messages.info(request, "Category added successfully.")
        category_data = Category.objects.all()

        return render(request, self.template_name,
                      {"category_data": category_data})


@method_decorator(login_required, name="dispatch")
class CategoryStatusView(generic.TemplateView):
    template_name = 'bestof-admin/manage-food-category/index.html'

    def post(self, request, *args, **kwargs):

        categorystatusid = request.POST["categorystatusid"]
        categorystatus = request.POST["categorystatus"]
        if categorystatus == "True":
            status = False
        else:
            status = True
        Category.objects.filter(id=categorystatusid).update(publish_status=status)
        # messages.info(request, "Status Changed successfully.")
        check_map = 1
        return JsonResponse({'categorystatusid': check_map})

@method_decorator(login_required, name="dispatch")
class EditFoodCategoryView(generic.TemplateView):
    template_name = 'bestof-admin/manage-food-category/edit.html'

    def get(self, request, id, *args, **kwargs):
        category_instance = get_object_or_404(Category, id=id)
        food_category_form = FoodCategoryForm(instance=category_instance)
        return render(request, self.template_name,
                      {'category_data': category_instance, 'food_category_form': food_category_form})

    def post(self, request, id, *args, **kwargs):
        category_instance = get_object_or_404(Category, id=id)
        food_category_form = FoodCategoryForm(request.POST, instance=category_instance)
        if food_category_form.is_valid():
            food_category_form.save()

            return HttpResponseRedirect(reverse('manage_food_category_link:ManageFoodCategoryView'))
#
@method_decorator(login_required, name="dispatch")
class FoodCategoryDeleteView(generic.TemplateView):
    template_name = 'bestof-admin/manage-food-category'


    def post(self, request,  *args, **kwargs):
        get_id = request.POST["id_log"]
        if get_id:
            if Category.objects.filter(id=get_id).exists():
                Category.objects.filter(id=get_id).delete()
        return HttpResponseRedirect(reverse('manage_food_category_link:ManageFoodCategoryView'))
#
