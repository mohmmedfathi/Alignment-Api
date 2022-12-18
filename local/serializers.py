from rest_framework import serializers
from . import models

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Local_Model
        fields = '__all__'
