from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy
from custom_user.models import User
import django


class Delivery_Partner(models.Model):
    name = models.CharField(ugettext_lazy('Name'), max_length=150, blank=True, null=True, db_column="name")

    slug = AutoSlugField(populate_from='name', always_update=True, unique_with='created_dt__month', db_column="slug",
                         null=True, blank=True)

    publish_status = models.BooleanField(ugettext_lazy('Publish Status'), default=True, db_column="publish_status")


    logo = models.ImageField(ugettext_lazy('Logo'), default="defalut_partner_logo.png", blank=True, null=True, db_column="logo",
                                   upload_to='business/delivery/')

    deep_link_url = models.CharField(ugettext_lazy('Deep Link URL'), max_length=150, blank=True, null=True, db_column="deep_link_url")

    created_by = models.ForeignKey(User, related_name='delivery_link_created_by', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)


    def __str__(self):
        return self.name  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Delivery Master"  # display table name for admin
        db_table = 'Delivery_Master'  # display table name for admin
