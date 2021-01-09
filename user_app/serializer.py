# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
# Import user model form Custom User application.
from custom_user.models import User


# Create serializer for User Registration.
class UserRegistrationSerializers(serializers.ModelSerializer):
    # Attach user model for store data in user table.
    full_name = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)
    location = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['full_name','email','location','password']

    # Create a validate function for insert data into table.
    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        full_name = data.get("full_name", "")
        location = data.get("location", "")
        if User.objects.filter(email=email).exists():  # Check email already registered or not.
            mes = "Email already exist."  # Message if user already registered.
            raise exceptions.APIException(mes)  # Call message if user already registered.
        else:  # Do if user not registered.
            User_Set = User(
                full_name = full_name,
                email=email,
                location=location,
                is_active=False,
            )  # Insert value in user table according to filed name.
            User_Set.set_password(password)  # Set password for user registration.
            User_Set.save()  # Save user data into table.
            return User_Set  # Return some information according to function.
# ======================================================================================================================


# Create serializer for User Login.
class UserLoginSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        if User.objects.filter(email=email).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, email=email)
            if user_instance.is_active == True:  # Check account is active or not.
                user = authenticate(email=email, password=password)
                if user is not None:  # Check login detail valid or not.
                    return user  # Return some information according to function.
                else:
                    mes = "Invalid login detail."  # Message if invalid login detail.
                    raise exceptions.APIException(mes)  # Call message if invalid login detail.
            else:
                mes = "Account not activate."  # Message if invalid login detail.
                raise exceptions.APIException(mes)  # Call message if invalid login detail.
        else:
            mes = "Email not register."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================


# Create serializer for User Activate function.
class UserActivateSerializers(serializers.Serializer):
    # Create some field for User Activate like email, password.
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)
    otp = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Activate.
    def validate(self, data):
        email = data.get("email", "")
        otp = data.get("otp", "")
        if User.objects.filter(email=email).exists():  # Check email already registered or not.
            user_instance = get_object_or_404(User, email=email)  # Get user instance if user already registered.
            if otp == str(user_instance.otp):  # Check OTP is valid or not.
                User.objects.filter(email=email).update(otp=None, is_active=True)  # Update otp value and active user.
                return user_instance  # Return some information according to function.
            else:
                mes = "Invalid OTP."  # Message if invalid login detail.
                raise exceptions.APIException(mes)  # Call message if invalid login detail.
        else:
            mes = "Email not register."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================
