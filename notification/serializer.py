# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
# Import user model form Custom User application.
from notification.models import Notification
from custom_user.models import User
from category_app.models import Category



class GetNotificationInfoSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('message','user_name','user','user_image','post', 'owner', 'created_dt')

    def get_user_image(self, obj):
        if obj.user.user_image:
            return obj.user.user_image.url
        else:
            return "No Image"


# Create serializer for Get Self Post Information.
class NotificationSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        user_id = data.get("user_id", "")
        if User.objects.filter(id=user_id).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, id=user_id)
            return user_instance
        else:
            mes = "User not exist.."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================
