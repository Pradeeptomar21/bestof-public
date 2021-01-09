# Import Python Packages.
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Import user define packages.Business_Details
from .serializer import GetPostInfoSerializer, SelfPostInfoSerializers, BusinessPostInfoSerializers
from BestofProject.tokens import CsrfExemptSessionAuthentication
from business_detail.models import Business_categories, Business_Details, Business_Photos, Business_Time, Business_Posts, Post_Activity
from category_app.models import Category

# Create class for business vote.
class GetPostInfoView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            post_detail = Business_Posts.objects.all().order_by("-id")
            get_data = GetPostInfoSerializer(post_detail, many=True)
            data = get_data.data
            data_response = {'detail': "Get Post Information.", 'status': 1, 'data': data}
            return Response(data_response)


# Create class for business vote.
class SelfPostInfoView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = SelfPostInfoSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                post_vote_detail = Business_Posts.objects.filter(created_by=serializer.validated_data).order_by("-id")
                post_like_detail = Business_Posts.objects.filter(
                    post_activity_for__created_by=serializer.validated_data).order_by("-id")

                post_detail_value = post_vote_detail | post_like_detail
                get_data = GetPostInfoSerializer(post_detail_value, many=True)
                data = get_data.data

                total_vote = Post_Activity.objects.filter(created_by = serializer.validated_data).filter(Vote=True).count()
                total_like = Post_Activity.objects.filter(created_by = serializer.validated_data).filter(Like=True).count()
                if serializer.validated_data.user_image:
                    image = serializer.validated_data.user_image.url
                else:
                    image = "no image"
                data_response = {'detail': "Get Post Information.", 'status': 1,'image':image,'name':serializer.validated_data.full_name,'about_me':serializer.validated_data.about_me, 'data': data, 'total_vote': total_vote, 'total_like': total_like}
                return Response(data_response)


# Create class for business vote.
class BusinessPostInfoView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = BusinessPostInfoSerializers(data=request.data)  # Call serializer function created by user.
            data = []
            if serializer.is_valid():  # Get data if serializer is valid.
                business_id = serializer.validated_data['business_id']
                category_id = serializer.validated_data['category_name']

                business_instance = get_object_or_404(Business_Details, id=business_id)
                category_instance = get_object_or_404(Category, id=category_id)

                post_detail = Business_Posts.objects.filter(Business_id=business_instance).filter(~Q(Category_id = category_instance))
                # post_detail = Business_Posts.objects.all().values('Category_id').distinct()
                if post_detail:
                    value = []
                    for data in post_detail:
                        if data.Category_id in value:
                            pass
                        else:
                            value.append(data.Category_id)
                    category_instance = get_object_or_404(Category, name=value[0])
                    post_value = Business_Posts.objects.filter(Business_id=business_instance).filter(
                        Category_id=category_instance).order_by("-id")[:1]

                    for cat_data in value:
                        category_instance = get_object_or_404(Category, name=cat_data)
                        post_detail = Business_Posts.objects.filter(Business_id=business_instance).filter(Category_id=category_instance).order_by("-id")[:1]
                        if post_detail in post_value:
                            pass
                        else:
                            post_value = post_value | post_detail
                    print(post_value)

                    get_data = GetPostInfoSerializer(post_value, many=True)
                    data = get_data.data

                data_response = {'detail': "Get Post Information.", 'status': 1, 'data': data}
                return Response(data_response)