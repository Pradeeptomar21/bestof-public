from django.db import models
from django.utils.translation import ugettext_lazy
from autoslug import AutoSlugField
import django
# Import user model form Custom User application.
from custom_user.models import User


class Tag(models.Model):
    name = models.CharField(ugettext_lazy('Name'), max_length=50, blank=True, null=True, db_column="name")
    slug = AutoSlugField(populate_from='name', always_update=True, unique_with='created_dt__month', db_column="slug",
                         null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='tag_created_by', on_delete=models.CASCADE,
                                    null=True, blank=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.name  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Tag"  # display table name for admin
        db_table = 'Tag'  # display table name for admin


class Category(models.Model):
    name = models.CharField(ugettext_lazy('Name'), max_length=50, blank=True, null=True, db_column="name")
    slug = AutoSlugField(populate_from='name', always_update=True, unique_with='created_dt__month', db_column="slug",
                         null=True, blank=True)
    publish_status = models.BooleanField(ugettext_lazy('Publish Status'), default=True, db_column="publish_status")
    food = models.CharField(ugettext_lazy('Food'), max_length=50, blank=True, null=True, db_column="food")
    created_by = models.ForeignKey(User, related_name='category_created_by', on_delete=models.CASCADE,
                                    null=True, blank=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    Tag = models.ForeignKey(Tag, related_name='category_tag', on_delete=models.CASCADE,
                            null=True, blank=True)

    def __str__(self):
        return self.name  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Category"  # display table name for admin
        db_table = 'Category'  # display table name for admin

