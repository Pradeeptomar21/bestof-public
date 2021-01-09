# Import python package.
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.files.base import ContentFile
import base64
from PIL import Image
# Import user model form Custom User application.
from .models import Category


class CategoryDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
