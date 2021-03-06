# Generated by Django 3.1.3 on 2020-11-23 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business_detail', '0007_auto_20201121_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Like', models.BooleanField(default=False)),
                ('Vote', models.BooleanField(default=False)),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_activity_for', to='business_detail.business_posts')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_activity_for', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_activity_created_by', to=settings.AUTH_USER_MODEL)),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_activity_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts Activity',
                'db_table': 'Posts_Activity',
            },
        ),
    ]
