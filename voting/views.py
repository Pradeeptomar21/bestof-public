from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from business_detail.models import Business_Details, Business_Posts, Post_Activity


# Create your views here.

@method_decorator(login_required, name="dispatch")
class VotingView(generic.TemplateView):
    template_name = 'bestof-admin/voting/index.html'

    def get(self, request, *args, **kwargs):
        vote_data = Business_Details.objects.all()

        return render(request, self.template_name,
                      {'vote_data': vote_data})


@method_decorator(login_required, name="dispatch")
class Voting_Details(generic.TemplateView):
    template_name = 'bestof-admin/voting/voting_detail.html'

    def get(self, request, id, *args, **kwargs):
        business_instance = get_object_or_404(Business_Details, business_id=id)
        business_data = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True)

        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})
