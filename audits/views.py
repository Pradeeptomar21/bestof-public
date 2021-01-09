from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from business_detail.models import Business_Details, Business_Posts, Post_Activity, Remove_Activity
from .models import Search_Keyword
from custom_user.models import User
from django.db.models import Q


# Create your views here.

@method_decorator(login_required, name="dispatch")
class AuditView(generic.TemplateView):
    template_name = 'bestof-admin/audits/index.html'

    def get(self, request, *args, **kwargs):

        filters = ~Q(created_dt=None)
        user_filters = ~Q(date_joined=None)
        start_date = ""
        if 'start-date' in request.GET:
            start_date = request.GET['start-date']
            filters = filters & Q(created_dt__gte=start_date)
            user_filters = user_filters & Q(date_joined__gte=start_date)

        end_date1 = ""
        if 'end-date' in request.GET:
            end_date1 = request.GET['end-date']
            end_date = str(request.GET['end-date']) + ' 23:59:59'
            filters = filters & Q(created_dt__lte=end_date)
            user_filters = user_filters & Q(date_joined__lte=end_date)

        vote_data = Post_Activity.objects.filter(Vote=True).filter(filters)
        like_data = Post_Activity.objects.filter(Like=True).filter(filters)
        remove_vote_data = Remove_Activity.objects.filter(type="Vote").filter(filters)
        remove_like_data = Remove_Activity.objects.filter(type="Like").filter(filters)
        Business_Posts_data = Business_Posts.objects.filter(filters)
        user_data = User.objects.filter(is_superuser=False).filter(user_filters)

        search_keyword_info = Search_Keyword.objects.filter(filters)
        search_keyword_data = []
        for data in search_keyword_info:
            search_keyword_data_new = data.keyword
            if search_keyword_data_new not in search_keyword_data:
                search_keyword_data.append(search_keyword_data_new)

        return render(request, self.template_name,
                      {'vote_data':vote_data,'like_data':like_data,'Business_Posts_data':Business_Posts_data,
                       'user_data':user_data,'remove_vote_data':remove_vote_data,'remove_like_data':remove_like_data,
                       'search_keyword_data':search_keyword_data,'start_date':start_date,'end_date':end_date1})


@method_decorator(login_required, name="dispatch")
class AuditDetailView(generic.TemplateView):
    template_name = 'bestof-admin/audits/view-detail.html'

    def get(self, request, *args, **kwargs):
        page_value = ""

        filters = ~Q(created_dt=None)
        user_filters = ~Q(date_joined=None)
        start_date = ""

        if 'start-date' in request.GET:
            start_date = request.GET['start-date']
            filters = filters & Q(created_dt__gte=start_date)
            user_filters = user_filters & Q(date_joined__gte=start_date)

        end_date1 = ""
        if 'end-date' in request.GET:
            end_date1 = request.GET['end-date']
            end_date = str(request.GET['end-date']) + ' 23:59:59'
            filters = filters & Q(created_dt__lte=end_date)
            user_filters = user_filters & Q(date_joined__lte=end_date)

        # vote_data = Post_Activity.objects.filter(Vote=True).filter(filters)

        like_data = Post_Activity.objects.filter(Like=True).filter(filters)
        remove_vote_data = Remove_Activity.objects.filter(type="Vote").filter(filters)
        remove_like_data = Remove_Activity.objects.filter(type="Like").filter(filters)
        Business_Posts_data = Business_Posts.objects.filter(filters)


        # vote_data = Business_Details.objects.all()
        vote_data=[]


        user_data = []
        search_keyword_data = []
        if 'detail-page' in request.GET:
            page_value = request.GET['detail-page']


        if page_value == 'vote':
            vote_info = Post_Activity.objects.filter(filters).filter(Vote=True)
            for data in vote_info:
                vote_data_new = data.Post_id.Business_id.business_id
                if vote_data_new not in vote_data:
                    vote_data.append(vote_data_new)

        if page_value == 'like':
            vote_info = Post_Activity.objects.filter(filters).filter(Like=True)
            for data in vote_info:
                vote_data_new = data.Post_id.Business_id.business_id
                if vote_data_new not in vote_data:
                    vote_data.append(vote_data_new)

        if page_value == 'post':
            vote_info = Business_Posts.objects.filter(filters)
            for data in vote_info:
                vote_data_new = data.Business_id.business_id
                if vote_data_new not in vote_data:
                    vote_data.append(vote_data_new)




        if page_value == 'user':
            user_info = User.objects.filter(is_superuser=False).filter(user_filters)

            # user_info = User.objects.filter(is_superuser=False)
            for data in user_info:
                user_data_new = data.location
                if user_data_new not in user_data:
                    user_data.append(user_data_new)

        elif page_value == 'search-keyword':
            search_keyword_info = Search_Keyword.objects.filter(filters)
            # search_keyword_info = Search_Keyword.objects.all()
            for data in search_keyword_info:
                search_keyword_data_new = data.keyword
                if search_keyword_data_new not in search_keyword_data:
                    search_keyword_data.append(search_keyword_data_new)

        return render(request, self.template_name,
                      {'page_value':page_value, 'vote_data':vote_data,'user_data':user_data,
                       'search_keyword_data':search_keyword_data,'start_date':start_date,'end_date':end_date1})


@method_decorator(login_required, name="dispatch")
class VoteDownView(generic.TemplateView):
    template_name = 'bestof-admin/audits/vote/remove-vote-detail.html'

    def get(self, request, *args, **kwargs):

        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)

            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Remove_Activity.objects.filter(Post_id__Business_id=business_instance).filter(filters).filter(type='Vote')
        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})


@method_decorator(login_required, name="dispatch")
class VoteUpView(generic.TemplateView):
    template_name = 'bestof-admin/audits/vote/voting-detail.html'

    def get(self, request, *args, **kwargs):

        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)


            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(filters).filter(Vote=True)

        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})


@method_decorator(login_required, name="dispatch")
class CategoryDetailView(generic.TemplateView):
    template_name = 'bestof-admin/audits/vote/category-detail.html'

    def get(self, request, *args, **kwargs):

        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)


            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(filters).filter(Vote=True)
            category_name = []
            for data in business_data:
                category_name_new = data.Post_id.Category_id.name
                if category_name_new not in category_name:
                    category_name.append(category_name_new)
                    # category_name = category_name + ", " + category_name_new

        return render(request, self.template_name,
                      {'business_instance': business_instance, 'category_name': category_name})


@method_decorator(login_required, name="dispatch")
class LikeDownView(generic.TemplateView):
    template_name = 'bestof-admin/audits/like/like-down-detail.html'

    def get(self, request,  *args, **kwargs):
        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)

            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Remove_Activity.objects.filter(Post_id__Business_id=business_instance).filter(filters).filter(type='Like')
        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})


@method_decorator(login_required, name="dispatch")
class LikeUpView(generic.TemplateView):
    template_name = 'bestof-admin/audits/like/like-up-detail.html'

    def get(self, request, *args, **kwargs):

        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)

            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(filters).filter(Like=True)

        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})

@method_decorator(login_required, name="dispatch")
class PostDetailView(generic.TemplateView):
    template_name = 'bestof-admin/audits/post/post-detail.html'

    def get(self, request, *args, **kwargs):
        if 'business-id' in request.GET:
            business_id = request.GET['business-id']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)



            business_instance = get_object_or_404(Business_Details, business_id=business_id)
            business_data = Business_Posts.objects.filter(filters).filter(Business_id=business_instance)

        return render(request, self.template_name,
                      {'business_instance': business_instance, 'business_data': business_data})

@method_decorator(login_required, name="dispatch")
class UserDetailView(generic.TemplateView):
    template_name = 'bestof-admin/audits/user/user-detail.html'

    def get(self, request, *args, **kwargs):
        if 'location' in request.GET:
            location = request.GET['location']

            user_filters = ~Q(date_joined=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                user_filters = user_filters & Q(date_joined__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                user_filters = user_filters & Q(date_joined__lte=end_date)

            user_data = User.objects.filter(location=location).filter(user_filters)
            return render(request, self.template_name,
                          {'user_data': user_data})

@method_decorator(login_required, name="dispatch")
class KeywordDetailView(generic.TemplateView):
    template_name = 'bestof-admin/audits/search-keyword/search-keyword.html'

    def get(self, request, *args, **kwargs):

        if 'keyword' in request.GET:
            keyword = request.GET['keyword']

            filters = ~Q(created_dt=None)
            if 'start-date' in request.GET:
                start_date = request.GET['start-date']
                filters = filters & Q(created_dt__gte=start_date)

            if 'end-date' in request.GET:
                end_date = str(request.GET['end-date']) + ' 23:59:59'
                filters = filters & Q(created_dt__lte=end_date)



            search_keyword_info = Search_Keyword.objects.filter(filters).filter(keyword=keyword)

        return render(request, self.template_name,
                      {'search_keyword_info': search_keyword_info})
