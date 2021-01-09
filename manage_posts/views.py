from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
# from admin_log_data.models import admin_add_log


# Create your views here.
from business_detail.models import Business_Posts, Post_Activity


@method_decorator(login_required, name="dispatch")
class ManagePostsView(generic.TemplateView):
    template_name = 'bestof-admin/manage-post/index.html'

    def get(self, request, *args, **kwargs):
        get_manage_post = Business_Posts.objects.all().order_by('-id')
        return render(request, self.template_name,
                      {'get_manage_post': get_manage_post})


@method_decorator(login_required, name="dispatch")
class PostStatusView(generic.TemplateView):
    template_name = 'bestof-admin/manage-post/index.html'

    def post(self, request, *args, **kwargs):

        poststatusid = request.POST["poststatusid"]
        poststatus = request.POST["poststatus"]
        if poststatus == "True":
            status = False
        else:
            status = True
        Business_Posts.objects.filter(id=poststatusid).update(publish_status=status)
        # messages.info(request, "Status Changed successfully.")
        check_map = 1
        return JsonResponse({'userstatusid': check_map})



@method_decorator(login_required, name="dispatch")
class PostDetailView(generic.TemplateView):
    template_name = 'bestof-admin/manage-post/view-detail.html'

    def get(self,  request,  *args, **kwargs):
        post_data=""
        post_instance=""
        if 'post-id' in request.GET:
            post_id = request.GET['post-id']

            post_instance = get_object_or_404(Business_Posts, id=post_id)
            post_data = Post_Activity.objects.filter(Post_id=post_instance).filter(Vote=True)





        #
        # post_instance = get_object_or_404(Business_Posts, id=id)
        # food_category_form = FoodCategoryForm(instance=category_instance)
        return render(request, self.template_name,
                      {'post_data':post_data,'post_instance':post_instance})
    #
    # def post(self, request, id, *args, **kwargs):
    #     category_instance = get_object_or_404(Category, id=id)
    #     food_category_form = FoodCategoryForm(request.POST, instance=category_instance)
    #     if food_category_form.is_valid():
    #         food_category_form.save()
    #
    #         return HttpResponseRedirect(reverse('manage_food_category_link:ManageFoodCategoryView'))
