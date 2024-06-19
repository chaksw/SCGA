from rest_framework import serializers
from .models import Scga


class ScgaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scga
        fields = ['id', 'file_name', 'baseline']
