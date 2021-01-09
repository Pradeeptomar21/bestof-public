# Generated by Django 3.1.3 on 2020-11-17 08:12

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='name', max_length=50, null=True, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, blank=True, db_column='slug', editable=False, null=True, populate_from='name', unique_with=('created_dt__month',))),
                ('business_id', models.CharField(blank=True, db_column='business_id', max_length=50, null=True, verbose_name='Business Id')),
                ('image_url', models.CharField(blank=True, db_column='image_url', max_length=50, null=True, verbose_name='Image URL')),
                ('business_display_address', models.TextField(blank=True, db_column='business_display_address', null=True, verbose_name='Business Display Address')),
                ('latitude', models.CharField(blank=True, db_column='latitude', max_length=50, null=True, verbose_name='Latitude')),
                ('longitude', models.CharField(blank=True, db_column='longitude', max_length=50, null=True, verbose_name='Longitude')),
                ('address1', models.CharField(blank=True, db_column='address1', max_length=50, null=True, verbose_name='Address1')),
                ('address2', models.CharField(blank=True, db_column='address2', max_length=50, null=True, verbose_name='Address2')),
                ('address3', models.CharField(blank=True, db_column='address3', max_length=50, null=True, verbose_name='Address3')),
                ('city', models.CharField(blank=True, db_column='city', max_length=50, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, db_column='country', max_length=50, null=True, verbose_name='Country')),
                ('state', models.CharField(blank=True, db_column='state', max_length=50, null=True, verbose_name='State')),
                ('zip_code', models.CharField(blank=True, db_column='zip_code', max_length=50, null=True, verbose_name='Zip Code')),
                ('cross_streets', models.CharField(blank=True, db_column='cross_streets', max_length=50, null=True, verbose_name='Cross Streets')),
                ('phone', models.CharField(blank=True, db_column='phone_number', max_length=50, null=True, verbose_name='Phone Number')),
                ('display_phone', models.CharField(blank=True, db_column='display_phone_number', max_length=50, null=True, verbose_name='Display Phone Number')),
                ('is_claimed', models.BooleanField(db_column='is_claimed', default=True, verbose_name='Is Claimed')),
                ('is_closed', models.BooleanField(db_column='is_closed', default=False, verbose_name='Is Closed')),
                ('transactions_pickup', models.BooleanField(db_column='transactions_pickup', default=False, verbose_name='Transactions Pickup')),
                ('transactions_delivery', models.BooleanField(db_column='transactions_delivery', default=False, verbose_name='Transactions Delivery')),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Business Info',
                'db_table': 'Business_Info',
            },
        ),
        migrations.CreateModel(
            name='Business_Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_overnight', models.BooleanField(default=False)),
                ('start', models.CharField(blank=True, db_column='start', max_length=50, null=True, verbose_name='Start')),
                ('end', models.CharField(blank=True, db_column='end', max_length=50, null=True, verbose_name='End')),
                ('day', models.CharField(blank=True, db_column='day', max_length=50, null=True, verbose_name='Day')),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_time_for', to='business_detail.business_details')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_time_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Business Time',
                'db_table': 'Business_Time',
            },
        ),
        migrations.CreateModel(
            name='Business_Photos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, db_column='url', max_length=50, null=True, verbose_name='Url')),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_photo_for', to='business_detail.business_details')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_photo_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Business Photo',
                'db_table': 'Business_Photo',
            },
        ),
        migrations.CreateModel(
            name='Business_categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_column='name', max_length=50, null=True, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, blank=True, db_column='slug', editable=False, null=True, populate_from='Slug', unique_with=('created_dt__month',))),
                ('publish_status', models.BooleanField(db_column='publish_status', default=False, verbose_name='Publish Status')),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Business_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_category_for', to='business_detail.business_details')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_category_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Business Categories',
                'db_table': 'Business_Categories',
            },
        ),
    ]