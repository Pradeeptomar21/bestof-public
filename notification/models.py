from django.db import models
from django.utils.translation import ugettext_lazy
from autoslug import AutoSlugField
import django
# Import user model form Custom User application.
from custom_user.models import User
from business_detail.models import Business_Posts


class Notification(models.Model):
    message = models.CharField(ugettext_lazy('Message'), max_length=50, blank=True, null=True, db_column="message")
    user_name = models.CharField(ugettext_lazy('User Name'), max_length=150, blank=True, null=True, db_column="user_name")
    user = models.ForeignKey(User, related_name='user_for_notification', on_delete=models.CASCADE)
    post = models.ForeignKey(Business_Posts, related_name='post_for_notification', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner_for_notification', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.message  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Notification"  # display table name for admin
        db_table = 'Notification'  # display table name for admin
