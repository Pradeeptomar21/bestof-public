# Import Python Packages.
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# Import user define packages.Business_Details
from .serializer import CategoryDetialSerializer
# from custom_user.models import User
from BestofProject.tokens import CsrfExemptSessionAuthentication
from .models import Category


# Create class for user registration.
class CategoryView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def get(self,request):
        category_detail = Category.objects.all().order_by("-id")
        get_data = CategoryDetialSerializer(category_detail, many=True)
        data = get_data.data
        data_response = {'detail': "Get Business Information.", 'status': 1, 'data': data}
        return Response(data_response)  # Send response as a API result.
# ======================================================================================================================

