from rest_framework import serializers
from home.models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'name', 'create', 'slug', 'update', 'image']
