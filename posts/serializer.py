    # Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
# Import user model form Custom User application.
from business_detail.models import Business_Time, Business_Photos, Business_Details, Business_categories, Business_Posts, Post_Activity
from custom_user.models import User
from category_app.models import Category



class PostActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Activity
        fields = ('id','User_id','Like','Vote')

class GetPostInfoSerializer(serializers.ModelSerializer):

    post_activity_for = PostActivitySerializer(many=True)
    vote_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Business_Posts
        fields = ('id','Business_id','Category_id','Tag_id','image','comment','owner_id','post_activity_for','vote_count','like_count')
        depth = 1

    def get_vote_count(self, obj):
        return obj.post_activity_for.filter(Vote=True).count()

    def get_like_count(self, obj):
        return obj.post_activity_for.filter(Like=True).count()
# ======================================================================================================================



# Create serializer for Get Self Post Information.
class SelfPostInfoSerializers(serializers.Serializer):
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


# Create serializer for Get Self Post Information.
class BusinessPostInfoSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    business_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    category_name = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        business_id = data.get("business_id", "")
        category_name = data.get("category_name", "")
        if Business_Details.objects.filter(business_id=business_id).exists():  # Check email already registered or not.
            if Category.objects.filter(name=category_name).exists():  # Check email already registered or not.
                business_instance = get_object_or_404(Business_Details, business_id=business_id)
                category_instance = get_object_or_404(Category, name=category_name)
                data["business_id"] = str(business_instance.id)
                data["category_name"] = str(category_instance.id)
                return data
            else:
                mes = "Category not exist.."  # Message if email not registered.
                raise exceptions.APIException(mes)  # Call message if email not registered.

        else:
            mes = "Business not exist.."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================
