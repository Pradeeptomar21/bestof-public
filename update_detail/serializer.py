# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
# Import user model form Custom User application.
from custom_user.models import User


# Create serializer for User Login.
class UpdatePasswordOtpSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        email = data.get("email", "")
        if User.objects.filter(email=email).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, email=email)
            return user_instance
        else:
            mes = "Email not register."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================


# Create serializer for User Login.
class UpdatePasswordSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)
    otp = serializers.CharField(style={"input_type": "text"}, write_only=True)
    # Create a validate function for Login.
    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        otp = data.get("otp", "")
        if User.objects.filter(email=email).filter(otp=otp).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, email=email)
            if user_instance.is_active == True :
                user_instance.set_password(password)
                user_instance.save()
                User.objects.filter(email=user_instance.email).update(otp=None)
                data['email']=email
                data['password']=password
                # data['user_instance']=user_instance
                return data
            else:
                mes = "Account not activate."  # Message if invalid login detail.
                raise exceptions.APIException(mes)  # Call message if invalid login detail.
        else:
            mes = "Invalid OTP."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================


# Create serializer for Update Profile.
class UpdateProfileSerializers(serializers.Serializer):
    # Create some field for Update Profile like user_id, full_name, user_image, about_me, distance.
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    full_name = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    user_image = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    about_me = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    distance = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)

    # Create a validate function for Profile.
    def validate(self, data):
        user_id = data.get("user_id", "")
        full_name = data.get("full_name", "")
        user_image = data.get("user_image", "")
        about_me = data.get("about_me", "")
        distance = data.get("distance", "")

        if User.objects.filter(id=user_id).exists():  # Check user already registered or not.
            user_instance = get_object_or_404(User, id=user_id)

            if full_name == "":  # Check full name is blank or not.
                full_name = user_instance.full_name  # If full name is blank then add old name.

            if distance == "":  # Check full distance is blank or not.
                distance = user_instance.distance  # If full distance is blank then add old distance.

            if user_instance.is_active:  # Check user active or not.
                User.objects.filter(id=user_id).update(
                    full_name=full_name,
                    about_me=about_me,
                    distance=distance,
                )  # update some profile detail.

                if user_image:   # Check user already registered or not.
                    # image upload function
                    data = ContentFile(base64.b64decode(user_image))
                    image = Image.open(data)
                    filetype = image.format
                    ext = filetype.lower()
                    today_date = date.today()
                    set_file_name = str(full_name) + str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year)
                    file_name = set_file_name + "." + ext
                    data = ContentFile(base64.b64decode(user_image), name=file_name)
                    user_instance = get_object_or_404(User, id=user_id)
                    user_instance.user_image = data
                    user_instance.save()
                return user_instance
            else:
                mes = "Account not activate."  # Message if invalid login detail.
                raise exceptions.APIException(mes)  # Call message if invalid login detail.
        else:
            mes = "User not exist."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================



# Create serializer for User Login.
class GetProfileDataSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    # Create a validate function for Login.
    def validate(self, data):
        user_id = data.get("user_id", "")
        if User.objects.filter(id=user_id).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, id=user_id)
            if user_instance.is_active == True :
                return user_instance
            else:
                mes = "Account not activate."  # Message if invalid login detail.
                raise exceptions.APIException(mes)  # Call message if invalid login detail.
        else:
            mes = "User not exists."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name','email','user_image','about_me','distance')

