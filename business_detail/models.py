from django.db import models
from django.utils.translation import ugettext_lazy
from autoslug import AutoSlugField
import django
# Import user model form Custom User application.
from custom_user.models import User
from category_app.models import Tag, Category
from manage_delivery_partner.models import Delivery_Partner


class Business_Details(models.Model):
    name = models.CharField(ugettext_lazy('Name'), max_length=50, blank=True, null=True, db_column="name")
    slug = AutoSlugField(populate_from='name', always_update=True, unique_with='created_dt__month', db_column="slug",
                         null=True, blank=True)
    business_id = models.CharField(ugettext_lazy('Business Id'), max_length=50, blank=True, null=True,
                                   db_column="business_id")
    image_url = models.CharField(ugettext_lazy('Image URL'), max_length=250, blank=True, null=True,
                                 db_column="image_url")
    business_display_address = models.TextField(ugettext_lazy('Business Display Address'), blank=True, null=True,
                                                db_column="business_display_address")
    latitude = models.CharField(ugettext_lazy('Latitude'), max_length=50, blank=True, null=True, db_column="latitude")
    longitude = models.CharField(ugettext_lazy('Longitude'), max_length=50, blank=True, null=True,
                                 db_column="longitude")
    address1 = models.CharField(ugettext_lazy('Address1'), max_length=50, blank=True, null=True, db_column="address1")
    address2 = models.CharField(ugettext_lazy('Address2'), max_length=50, blank=True, null=True, db_column="address2")
    address3 = models.CharField(ugettext_lazy('Address3'), max_length=50, blank=True, null=True, db_column="address3")
    city = models.CharField(ugettext_lazy('City'), max_length=50, blank=True, null=True, db_column="city")
    country = models.CharField(ugettext_lazy('Country'), max_length=50, blank=True, null=True, db_column="country")
    state = models.CharField(ugettext_lazy('State'), max_length=50, blank=True, null=True, db_column="state")
    zip_code = models.CharField(ugettext_lazy('Zip Code'), max_length=50, blank=True, null=True, db_column="zip_code")
    cross_streets = models.CharField(ugettext_lazy('Cross Streets'), max_length=50, blank=True, null=True,
                                     db_column="cross_streets")
    phone = models.CharField(ugettext_lazy('Phone Number'), max_length=50, blank=True, null=True,
                             db_column="phone_number")
    display_phone = models.CharField(ugettext_lazy('Display Phone Number'), max_length=50, blank=True, null=True,
                                     db_column="display_phone_number")
    is_claimed = models.BooleanField(ugettext_lazy('Is Claimed'), default=True, db_column="is_claimed")
    is_closed = models.BooleanField(ugettext_lazy('Is Closed'), default=False, db_column="is_closed")
    transactions_pickup = models.BooleanField(ugettext_lazy('Transactions Pickup'), default=False,
                                              db_column="transactions_pickup")
    transactions_delivery = models.BooleanField(ugettext_lazy('Transactions Delivery'), default=False,
                                                db_column="transactions_delivery")
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    total_vote = models.CharField(ugettext_lazy('Total Vote'), max_length=50, blank=True, null=True,
                             db_column="total_vote")
    total_like = models.CharField(ugettext_lazy('Total Like'), max_length=50, blank=True, null=True,
                             db_column="total_like")

    # = models.ManyToManyField(Ar_user, blank=True, related_name='user_data')

    dilevery_partner = models.ManyToManyField(Delivery_Partner,blank=True, related_name='dilevery_business_partner',
                             db_column="dilevery_partner")

    def __str__(self):
        return self.business_id  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Business Info"  # display table name for admin
        db_table = 'Business_Info'  # display table name for admin


class Business_categories(models.Model):
    title = models.CharField(ugettext_lazy('Title'), max_length=50, blank=True, null=True, db_column="title")
    alias = models.CharField(ugettext_lazy('Alias'), max_length=50, blank=True, null=True, db_column="alias")
    slug = AutoSlugField(populate_from='title', always_update=True, unique_with='created_dt__month', db_column="slug",
                         null=True, blank=True)
    publish_status = models.BooleanField(ugettext_lazy('Publish Status'), default=False, db_column="publish_status")
    Business_id = models.ForeignKey(Business_Details, related_name='business_category_for', on_delete=models.CASCADE,
                                    null=True, blank=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.title  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Business Categories"  # display table name for admin
        db_table = 'Business_Categories'  # display table name for admin


class Business_Photos(models.Model):
    url = models.CharField(ugettext_lazy('Url'), max_length=50, blank=True, null=True, db_column="url")
    business_image = models.ImageField(ugettext_lazy('Business Image'), blank=True, null=True,
                                       db_column="business_image",
                                       upload_to='business/image/')
    Business_id = models.ForeignKey(Business_Details, related_name='business_photo_for', on_delete=models.CASCADE)
    set_as_default = models.BooleanField(ugettext_lazy('Set as Default'), default=False, db_column="set_as_default")
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.url  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Business Photo"  # display table name for admin
        db_table = 'Business_Photo'  # display table name for admin


class Business_Time(models.Model):
    is_overnight = models.BooleanField(default=False)
    start = models.CharField(ugettext_lazy('Start'), max_length=50, blank=True, null=True, db_column="start")
    end = models.CharField(ugettext_lazy('End'), max_length=50, blank=True, null=True, db_column="end")
    day = models.CharField(ugettext_lazy('Day'), max_length=50, blank=True, null=True, db_column="day")
    Business_id = models.ForeignKey(Business_Details, related_name='business_time_for', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.day  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Business Time"  # display table name for admin
        db_table = 'Business_Time'  # display table name for admin


class Business_Posts(models.Model):
    Business_id = models.ForeignKey(Business_Details, related_name='business_post_for', on_delete=models.CASCADE)
    Category_id = models.ForeignKey(Category, related_name='category_post_for', on_delete=models.CASCADE)
    Tag_id = models.ForeignKey(Tag, related_name='tag_post_for', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(ugettext_lazy('Post Image'), blank=True, null=True, db_column="post_image",
                                   upload_to='business/post/')
    comment = models.CharField(ugettext_lazy('Comment'), max_length=250, blank=True, null=True,
                                 db_column="comment")
    owner_id = models.CharField(ugettext_lazy('Owner ID'), max_length=250, blank=True, null=True,
                                 db_column="owner_id")

    publish_status = models.BooleanField(ugettext_lazy('Publish Status'), default=True, db_column="publish_status")
    total_vote = models.CharField(ugettext_lazy('Total Vote'), max_length=50, default="0", blank=True, null=True,
                                  db_column="total_vote")
    created_by = models.ForeignKey(User, related_name='post_created_by', on_delete=models.CASCADE)
    update_by = models.ForeignKey(User, related_name='post_updated_by', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_dt = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        verbose_name_plural = "Business Posts"  # display table name for admin
        db_table = 'Business_Posts'  # display table name for admin


class Post_Activity(models.Model):
    Post_id = models.ForeignKey(Business_Posts, related_name='post_activity_for', on_delete=models.CASCADE)
    User_id = models.ForeignKey(User, related_name='post_activity_by', on_delete=models.CASCADE)
    Like = models.BooleanField(default=False)
    Vote = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='post_activity_created_by', on_delete=models.CASCADE)
    update_by = models.ForeignKey(User, related_name='post_activity_updated_by', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    update_dt = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        verbose_name_plural = "Posts Activity"  # display table name for admin
        db_table = 'Posts_Activity'  # display table name for admin


class Remove_Activity(models.Model):
    Post_id = models.ForeignKey(Business_Posts, related_name='remove_post_for', on_delete=models.CASCADE)
    User_id = models.ForeignKey(User, related_name='remove_by', on_delete=models.CASCADE)
    type = models.CharField(ugettext_lazy('Type'), max_length=50, blank=True, null=True,
                                 db_column="type")
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        verbose_name_plural = "Remove Activity"  # display table name for admin
        db_table = 'Remove_Activity'  # display table name for admin
