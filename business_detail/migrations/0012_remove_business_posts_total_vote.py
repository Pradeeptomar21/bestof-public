# Generated by Django 3.1.3 on 2020-12-05 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_detail', '0011_business_posts_total_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business_posts',
            name='total_vote',
        ),
    ]
