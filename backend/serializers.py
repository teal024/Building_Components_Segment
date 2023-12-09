from rest_framework import serializers
from backend.models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginalImage
        fields = '__all__'