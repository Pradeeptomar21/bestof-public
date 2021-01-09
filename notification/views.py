# Import Python Packages.
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# Import user define packages.Business_Details
from .serializer import NotificationSerializers, GetNotificationInfoSerializer
# from custom_user.models import User
from BestofProject.tokens import CsrfExemptSessionAuthentication
from .models import Notification


# Create class for business vote.
class NotificationAPIView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = NotificationSerializers(data=request.data)  # Call serializer function created by user.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                notification_detail = Notification.objects.filter(owner=serializer.validated_data).order_by("-id")
                get_data = GetNotificationInfoSerializer(notification_detail, many=True)
                data = get_data.data
                data_response = {'detail': "Get Notification Information.", 'status': 1, 'data': data}
                return Response(data_response)
