# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
from django.conf import settings
# Import user model form Custom User application.
from .models import Business_Time, Business_Photos, Business_Details, Business_categories, Business_Posts, Post_Activity, Remove_Activity
from audits.models import Search_Keyword
from custom_user.models import User
from category_app.models import Category
from notification.models import Notification


# Create serializer for Business Info.
class BusinessInfoSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    business_id = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        business_id = data.get("business_id", "")
        if business_id:
            return business_id
        else:
            mes = "Please Enter Business Id."  # Message if email not registered.
            raise exceptions.APIException(mes)  # Call message if email not registered.
# ======================================================================================================================


# Create serializer for Business Info.
class BusinessSearchSerializers(serializers.Serializer):
    # Create some field for User Login like email, password.
    name = serializers.CharField(style={"input_type": "text"}, write_only=True)
    latitude = serializers.CharField(style={"input_type": "text"}, write_only=True)
    longitude = serializers.CharField(style={"input_type": "text"}, write_only=True)
    distance = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Login.
    def validate(self, data):
        data['name'] = data.get("name", "")
        data['latitude'] = data.get("latitude", "")
        data['longitude'] = data.get("longitude", "")
        data['distance'] = data.get("distance", "")

        return data
# ======================================================================================================================


class BusinessCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_categories
        fields = ('title','alias')


class BusinessPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Photos
        fields = ('url',)


class BusinessTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Time
        fields = ('is_overnight','start','end','day')


class GetBusinessInfoSerializer(serializers.ModelSerializer):

    business_category_for = BusinessCategoriesSerializer(many=True)
    business_photo_for = BusinessPhotoSerializer(many=True)
    business_time_for = BusinessTimeSerializer(many=True)
    class Meta:
        model = Business_Details
        fields = ('business_id','name','image_url','phone','display_phone','business_display_address','address1','address2','address3','city','state','country','zip_code','cross_streets',
                  'latitude','longitude','transactions_pickup', 'transactions_delivery','business_category_for',
                  'business_photo_for','business_time_for','dilevery_partner','total_vote','total_like')
        depth = 1
# ======================================================================================================================


# Create serializer for Business Vote.
class BusinessVoteSerializers(serializers.Serializer):
    # Create some field for Vote.
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    business_id = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    category_name = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    force_to_vote = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    post_id = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    comment = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    image = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)

    # Create a validate function for Vote.
    def validate(self, data):
        business_id = data.get("business_id", "")
        category_name = data.get("category_name", "")
        user_id = data.get("user_id", "")
        post_id = data.get("post_id", "")
        force_to_vote = data.get("force_to_vote", "")
        comment = data.get("comment", "")
        if force_to_vote == "":  # Check vote forcefully or not.
            force_to_vote = False
        if User.objects.filter(id=user_id).exists():  # Check user exist or not.
            user_instance = get_object_or_404(User, id=user_id)
        else:
            mes = "User not exists."  # Message if user not exist.
            raise exceptions.APIException(mes)  # Call message if user not exist.

        if Business_Details.objects.filter(business_id=business_id).exists():  # Check business exist or not.
            business_instance = get_object_or_404(Business_Details, business_id=business_id)
        else:
            mes = "Business not exists."  # Message if business not exist.
            raise exceptions.APIException(mes)  # Call message if business not exist.

        category_name = category_name.lower()  # Convert category name into lower case.
        if Category.objects.filter(name=category_name).exists():  # Check Category exist or not.
            category_instance = get_object_or_404(Category, name=category_name)
        else:
            category_instance = Category(name=category_name, created_by=user_instance)  # If category not exist.
            category_instance.save()  # Save category into table.

        if not force_to_vote:  # If vote is not forcefully.
            post_data = Post_Activity.objects.filter(User_id=user_instance).filter(Vote=True)  # Get user voting list.
            for get_data in post_data:
                if category_instance == get_data.Post_id.Category_id:  # Check user already voted on same category.
                    mes = "Already voted on another post."  # Message if already voted.
                    raise exceptions.APIException(mes)  # Call message if already voted.

            if post_id:  # Check post id given or not.
                if Business_Posts.objects.filter(id=post_id).exists():  # check business post available.
                    business_post_instance = get_object_or_404(Business_Posts, id=post_id)  # get post instance.
                    Post_Set = Business_Posts(
                        Business_id=business_post_instance.Business_id,
                        Category_id=business_post_instance.Category_id,
                        comment=business_post_instance.comment,
                        image=business_post_instance.image,
                        owner_id = str(user_instance.id),
                        created_by=user_instance,
                        update_by=user_instance,
                    )  # Insert value in business post table according to filed name.
                    Post_Set.save()  # Save post data into table.

                    Post_Activity_Set = Post_Activity(
                        Post_id=business_post_instance,
                        User_id=user_instance,
                        Vote=True,
                        created_by=user_instance,
                        update_by=user_instance,
                    )  # Insert value in post activity table according to filed name.
                    Post_Activity_Set.save()  # Save post activity into table.
                    Notification_Set = Notification(
                        message= user_instance.full_name + " vote your post.",
                        user_name=user_instance.full_name,
                        user=user_instance,
                        post=business_post_instance,
                        owner=business_post_instance.created_by,
                    )
                    Notification_Set.save()
                    count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True).count()
                    Business_Details.objects.filter(business_id=business_id).update(total_vote=count)

                    cat_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Post_id__Category_id=category_instance).filter(Vote=True).count()
                    Business_Posts.objects.filter(Business_id=business_instance).filter(Category_id=category_instance).update(total_vote=cat_count)


            else:  # If post id not given.
                image = data.get("image", "")
                Post_Set = Business_Posts(
                    Business_id=business_instance,
                    Category_id=category_instance,
                    comment=comment,
                    owner_id=str(user_instance.id),
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in business post table according to filed name.
                Post_Set.save()  # Save post data into table.

                if image:  # If post image avilable.
                    # image upload function
                    data = ContentFile(base64.b64decode(image))
                    get_image = Image.open(data)
                    filetype = get_image.format
                    ext = filetype.lower()
                    today_date = date.today()
                    set_file_name = str(business_id) + str(today_date.day) + "_" + str(today_date.month) + "_" + str(
                        today_date.year)
                    file_name = set_file_name + "." + ext
                    data = ContentFile(base64.b64decode(image), name=file_name)
                    Post_Set.image = data
                    Post_Set.save()

                    # ---------------------------------------
                    photos_info = Business_Photos(url=settings.IMAGE_BASE_URL + Post_Set.image.url, Business_id=business_instance
                                                  )
                    photos_info.save()
                #     --------------------------------------------

                Post_Activity_Set = Post_Activity(
                    Post_id=Post_Set,
                    User_id=user_instance,
                    Vote=True,
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in post activity table according to filed name.
                Post_Activity_Set.save()  # Save post activity into table.

                # Notification_Set = Notification(
                #     message= user_instance.full_name + " vote your post.",
                #     user_name=user_instance.full_name,
                #     user=user_instance,
                #     post=Post_Set,
                #     owner=Post_Set.created_by,
                # )
                # Notification_Set.save()
                count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True).count()
                Business_Details.objects.filter(business_id=business_id).update(total_vote=count)

                cat_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(
                    Post_id__Category_id=category_instance).filter(Vote=True).count()
                Business_Posts.objects.filter(Business_id=business_instance).filter(
                    Category_id=category_instance).update(total_vote=cat_count)


        else:  # If vote is forcefully.
            post_data = Post_Activity.objects.filter(User_id=user_instance).filter(Vote=True)  # Get user voting list.
            for get_data in post_data:
                if category_instance == get_data.Post_id.Category_id:  # Check user already voted on same category.
                    Post_Activity.objects.filter(id=get_data.id).update(Vote=False) # Remove vote from post.

                    post_activity_instance = get_object_or_404(Post_Activity, id=get_data.id)

                    Notification_Set = Notification(
                        message=user_instance.full_name + " remove vote from your post.",
                        user_name=user_instance.full_name,
                        user=user_instance,
                        post=post_activity_instance.Post_id,
                        owner=post_activity_instance.Post_id.created_by,
                    )
                    Notification_Set.save()

                    Remove_Set = Remove_Activity(
                        Post_id=post_activity_instance.Post_id,
                        User_id=post_activity_instance.Post_id.created_by,
                        type="Vote",
                    )
                    Remove_Set.save()



                    count = Post_Activity.objects.filter(Post_id__Business_id=post_activity_instance.Post_id.Business_id).filter(
                        Vote=True).count()
                    Business_Details.objects.filter(business_id=post_activity_instance.Post_id.Business_id.business_id).update(total_vote=count)


                    cat_count = Post_Activity.objects.filter(Post_id__Business_id=post_activity_instance.Post_id.Business_id).filter(
                        Post_id__Category_id=post_activity_instance.Post_id.Category_id).filter(Vote=True).count()
                    Business_Posts.objects.filter(Business_id=post_activity_instance.Post_id.Business_id).filter(
                        Category_id=post_activity_instance.Post_id.Category_id).update(total_vote=cat_count)


            if post_id:  # Check post id given or not.
                if Business_Posts.objects.filter(id=post_id).exists():  # check business post available.
                    business_post_instance = get_object_or_404(Business_Posts, id=post_id)  # get post instance.
                    Post_Set = Business_Posts(
                        Business_id=business_post_instance.Business_id,
                        Category_id=business_post_instance.Category_id,
                        comment=business_post_instance.comment,
                        image=business_post_instance.image,
                        owner_id=str(user_instance.id),
                        created_by=user_instance,
                        update_by=user_instance,
                    )  # Insert value in business post table according to filed name.
                    Post_Set.save()  # Save post data into table.

                    Post_Activity_Set = Post_Activity(
                        Post_id=business_post_instance,
                        User_id=user_instance,
                        Vote=True,
                        created_by=user_instance,
                        update_by=user_instance,
                    )  # Insert value in post activity table according to filed name.
                    Post_Activity_Set.save()  # Save post activity data into table.

                    Notification_Set = Notification(
                        message=user_instance.full_name + " vote your post.",
                        user_name=user_instance.full_name,
                        user=user_instance,
                        post=business_post_instance,
                        owner=business_post_instance.created_by,
                    )
                    Notification_Set.save()
                    count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True).count()
                    Business_Details.objects.filter(business_id=business_id).update(total_vote=count)

                    cat_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(
                        Post_id__Category_id=category_instance).filter(Vote=True).count()
                    Business_Posts.objects.filter(Business_id=business_instance).filter(
                        Category_id=category_instance).update(total_vote=cat_count)



            else:  # If post id not given.
                image = data.get("image", "")
                Post_Set = Business_Posts(
                    Business_id=business_instance,
                    Category_id=category_instance,
                    comment=comment,
                    owner_id=str(user_instance.id),
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in business post table according to filed name.
                Post_Set.save()  # Save post data into table.

                if image:  # If post image avilable.
                    # image upload function
                    data = ContentFile(base64.b64decode(image))
                    get_image = Image.open(data)
                    filetype = get_image.format
                    ext = filetype.lower()
                    today_date = date.today()
                    set_file_name = str(business_id) + str(today_date.day) + "_" + str(today_date.month) + "_" + str(
                        today_date.year)
                    file_name = set_file_name + "." + ext
                    data = ContentFile(base64.b64decode(image), name=file_name)
                    Post_Set.image = data
                    Post_Set.save()

                    # ---------------------------------------
                    photos_info = Business_Photos(url=settings.IMAGE_BASE_URL + Post_Set.image.url,
                                                  Business_id=business_instance
                                                  )
                    photos_info.save()
                #     --------------------------------------------

                Post_Activity_Set = Post_Activity(
                    Post_id=Post_Set,
                    User_id=user_instance,
                    Vote=True,
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in post activity table according to filed name.
                Post_Activity_Set.save()  # Save post activity into table.

                # Notification_Set = Notification(
                #     message=user_instance.full_name + " vote your post.",
                #     user_name=user_instance.full_name,
                #     user=user_instance,
                #     post=Post_Set,
                #     owner=Post_Set.created_by,
                # )
                # Notification_Set.save()
        #         ---------------------------------
                count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(Vote=True).count()
                # business_instance.update(total_vote=count)
                Business_Details.objects.filter(business_id=business_id).update(total_vote=count)

                cat_count = Post_Activity.objects.filter(Post_id__Business_id=business_instance).filter(
                    Post_id__Category_id=category_instance).filter(Vote=True).count()
                Business_Posts.objects.filter(Business_id=business_instance).filter(
                    Category_id=category_instance).update(total_vote=cat_count)


        return user_id
# ======================================================================================================================


# Create serializer for Business Like.
class BusinessLikeSerializers(serializers.Serializer):
    # Create some field for like.
    post_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    like = serializers.BooleanField()
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for Like.
    def validate(self, data):
        post_id = data.get("post_id", "")
        like = data.get("like", True)
        user_id = data.get("user_id", "")

        if User.objects.filter(id=user_id).exists():  # Check user exist or not.
            user_instance = get_object_or_404(User, id=user_id)
        else:
            mes = "User not exists."  # Message if user not exist.
            raise exceptions.APIException(mes)  # Call message if user not exist.

        if Business_Posts.objects.filter(id=post_id).exists():  # Check business post exist or not.
            post_instance = get_object_or_404(Business_Posts, id=post_id)
        else:
            mes = "Post not exists."  # Message if business post not exist.
            raise exceptions.APIException(mes)  # Call message if business post not exist.

        if like == True:  # Check like is true.
            if Post_Activity.objects.filter(Post_id=post_instance).filter(User_id=user_instance).exists():  # user already like or vote on this post.
                Post_Activity.objects.filter(Post_id=post_instance).filter(User_id=user_instance).update(Like=True)  # Update user like on this post.
                Notification_Set = Notification(
                    message=user_instance.full_name + " like your post.",
                    user_name = user_instance.full_name,
                    user = user_instance,
                    post = post_instance,
                    owner=post_instance.created_by,
                )
                Notification_Set.save()

                count = Post_Activity.objects.filter(Post_id=post_instance).filter(Like=True).count()
                # business_instance.update(total_vote=count)
                Business_Details.objects.filter(business_id=post_instance.Business_id.business_id).update(total_like=count)

            else:  # If post activity not available.
                Post_Activity_Set = Post_Activity(
                    Post_id=post_instance,
                    User_id=user_instance,
                    Like=True,
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in post activity table according to filed name.
                Post_Activity_Set.save()  # Save post activity into table.

                Notification_Set = Notification(
                    message=user_instance.full_name + " like your post.",
                    user_name = user_instance.full_name,
                    user = user_instance,
                    post = post_instance,
                    owner=post_instance.created_by,
                )
                Notification_Set.save()

                count = Post_Activity.objects.filter(Post_id=post_instance).filter(Like=True).count()
                # business_instance.update(total_vote=count)
                Business_Details.objects.filter(business_id=post_instance.Business_id.business_id).update(total_like=count)
            display_message = "Like successfully."  # Display message if like post.
        else:  # Check like is false.
            if Post_Activity.objects.filter(Post_id=post_instance).filter(User_id=user_instance).exists():  # user already like or vote on this post.
                Post_Activity.objects.filter(Post_id=post_instance).filter(User_id=user_instance).update(Like=False)   # Update user like on this post.
                Notification_Set = Notification(
                    message=user_instance.full_name + " dislike your post.",
                    user_name=user_instance.full_name,
                    user=user_instance,
                    post=post_instance,
                    owner=post_instance.created_by,
                )
                Notification_Set.save()
                Remove_Set = Remove_Activity(
                    Post_id=post_instance,
                    User_id=post_instance.created_by,
                    type="Like",
                )
                Remove_Set.save()

                count = Post_Activity.objects.filter(Post_id=post_instance).filter(Like=True).count()
                # business_instance.update(total_vote=count)
                Business_Details.objects.filter(business_id=post_instance.Business_id.business_id).update(total_like=count)
            else:  # If post activity not available.
                Post_Activity_Set = Post_Activity(
                    Post_id=post_instance,
                    User_id=user_instance,
                    Like=False,
                    created_by=user_instance,
                    update_by=user_instance,
                )  # Insert value in post activity table according to filed name.
                Post_Activity_Set.save()  # Save post activity into table.
                Notification_Set = Notification(
                    message=user_instance.full_name + " dislike your post.",
                    user_name=user_instance.full_name,
                    user=user_instance,
                    post=post_instance,
                    owner=post_instance.created_by,
                )
                Notification_Set.save()
                Remove_Set = Remove_Activity(
                    Post_id=post_instance,
                    User_id=post_instance.created_by,
                    type="Like",
                )
                Remove_Set.save()

                count = Post_Activity.objects.filter(Post_id=post_instance).filter(Like=True).count()
                # business_instance.update(total_vote=count)
                Business_Details.objects.filter(business_id=post_instance.Business_id.business_id).update(total_like=count)
            display_message = "Dislike successfully."  # Display message if like post.
        return display_message  # Return display message.
# ======================================================================================================================


# Create serializer for Search Keyword.
class SearchKeywordSerializers(serializers.Serializer):
    # Create some field for search keyword.
    keyword = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # Create a validate function for search keyword.
    def validate(self, data):
        keyword = data.get("keyword", "")
        keyword = keyword.lower()
        keyword = Search_Keyword(keyword=keyword)
        keyword.save()
        return "Added"  # Return display message.
# ======================================================================================================================