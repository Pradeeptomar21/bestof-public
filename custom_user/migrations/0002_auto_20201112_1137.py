# Generated by Django 3.1.3 on 2020-11-12 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(blank=True, db_column='user_image', null=True, upload_to='user/profile/', verbose_name='Profile Image'),
        ),
    ]