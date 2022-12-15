from rest_framework import serializers
from . import models

class GlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Global_Model
        fields = '__all__'
