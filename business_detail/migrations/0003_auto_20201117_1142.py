# Generated by Django 3.1.3 on 2020-11-17 11:42

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_detail', '0002_auto_20201117_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_categories',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, blank=True, db_column='slug', editable=False, null=True, populate_from='title', unique_with=('created_dt__month',)),
        ),
    ]