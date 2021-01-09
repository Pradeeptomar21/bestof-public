from django.db import models
from django.utils.translation import ugettext_lazy
import django


class Search_Keyword(models.Model):
    keyword = models.CharField(ugettext_lazy('Keyword'), max_length=250, blank=True, null=True, db_column="keyword")
    created_dt = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.keyword  # return value when call model as primary key

    class Meta:
        verbose_name_plural = "Search Keyword"  # display table name for admin
        db_table = 'Search_Keyword'  # display table name for admin
