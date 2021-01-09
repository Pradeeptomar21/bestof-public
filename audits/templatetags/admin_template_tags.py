from django.shortcuts import get_object_or_404
from django import template
from business_detail.models import Business_Details, Business_Posts, Post_Activity, Remove_Activity
from custom_user.models import User
from audits.models import Search_Keyword
from django.db.models import Q
register = template.Library()

@register.simple_tag
def total_category_by_business(pk):
    total_category = 0
    business_instance = get_object_or_404(Business_Details, business_id=pk)
    business_data = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True)
    category_name = []
    for data in business_data:
        category_name_new = data.Post_id.Category_id.name
        if category_name_new not in category_name:
            category_name.append(category_name_new)

    total_category = len(category_name)

    return (total_category)


@register.simple_tag
def post_owner_name(pk):
    user_instance = get_object_or_404(User, id=pk)
    return (user_instance)

@register.simple_tag
def post_voted_by(pk):
    post_instance = get_object_or_404(Business_Posts, id=pk)
    post_data = Post_Activity.objects.filter(Post_id=post_instance).filter(Vote=True).count()
    # user_name = ""
    # for data in post_data:
    #     if user_name:
    #         user_name = user_name + "|" + data.User_id.full_name
    #     else:
    #         user_name = data.User_id.full_name

    return (post_data)

@register.simple_tag
def total_dislike_data(pk):
    post_instance = get_object_or_404(Business_Details, id=pk)

    post_data = Business_Posts.objects.filter(Business_id=post_instance)
    vote_down_count = 0
    for data in post_data:
        post_instance = get_object_or_404(Business_Posts, id=data.id)
        vote_down_count = vote_down_count  + Remove_Activity.objects.filter(Post_id=post_instance).filter(type='Like').count()
    return (vote_down_count)


@register.simple_tag
def get_total_like_data(pk, start_date, end_date):
    business_instance = get_object_or_404(Business_Details, business_id=pk)
    filters = ~Q(created_dt=None)
    if start_date:
        filters = filters & Q(created_dt__gte=start_date)
    if end_date:
        end_date = end_date + ' 23:59:59'
        filters = filters & Q(created_dt__lte=end_date)
    post_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Like=True).filter(filters).count()

    return (post_count)

@register.simple_tag
def get_total_vote_data(pk, start_date, end_date):
    business_instance = get_object_or_404(Business_Details, business_id=pk)
    filters = ~Q(created_dt=None)
    if start_date:
        filters = filters & Q(created_dt__gte=start_date)
    if end_date:
        end_date = end_date + ' 23:59:59'
        filters = filters & Q(created_dt__lte=end_date)
    post_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True).filter(filters).count()
    return (post_count)


@register.simple_tag
def total_remove_vote(pk, start_date, end_date):
    business_instance = get_object_or_404(Business_Details, business_id=pk)
    filters = ~Q(created_dt=None)
    if start_date:
        filters = filters & Q(created_dt__gte=start_date)
    if end_date:
        end_date = end_date + ' 23:59:59'
        filters = filters & Q(created_dt__lte=end_date)

    # post_data = Business_Posts.objects.filter(Business_id=post_instance)

    post_count = Remove_Activity.objects.filter(Post_id__Business_id=business_instance).filter(type='Vote').filter(
        filters).count()

    # vote_down_count = 0
    # for data in post_data:
    #     post_instance = get_object_or_404(Business_Posts, id=data.id)
    #     vote_down_count = vote_down_count  + Remove_Activity.objects.filter(Post_id=post_instance).filter(type='Vote').count()
    return (post_count)

@register.simple_tag
def total_post_data(pk, start_date, end_date):
    business_instance = get_object_or_404(Business_Details, business_id=pk)
    filters = ~Q(created_dt=None)
    if start_date:
        filters = filters & Q(created_dt__gte=start_date)
    if end_date:
        end_date = end_date + ' 23:59:59'
        filters = filters & Q(created_dt__lte=end_date)
    post_count = Business_Posts.objects.filter(Business_id=business_instance).filter(filters).count()
    return (post_count)

@register.simple_tag
def get_business_name(pk):
    post_instance = get_object_or_404(Business_Details, business_id=pk)

    name = post_instance.name
    return (name)


@register.simple_tag
def total_like_data(pk):
    business_instance = get_object_or_404(Business_Details, id=pk)

    # post_data = Business_Posts.objects.filter(Business_id=post_instance)
    # vote_down_count = 0
    # for data in post_data:
    #     business_instance = get_object_or_404(Business_Details, business_id=data.id)
    vote_down_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Like=True).count()
        #
        #
        # post_instance = get_object_or_404(Business_Posts, id=data.id)
        # vote_down_count = vote_down_count  + Remove_Activity.objects.filter(Post_id=post_instance).filter(type='Like').count()
    return (vote_down_count)



@register.simple_tag
def total_user_by_location(location):
    # post_instance = get_object_or_404(Business_Details, id=pk)

    user_count = User.objects.filter(location=location).count()
    return (user_count)

@register.simple_tag
def total_keyword_search(keyword):
    total_search = Search_Keyword.objects.filter(keyword=keyword).count()
    return (total_search)
