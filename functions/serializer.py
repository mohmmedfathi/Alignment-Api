from rest_framework import serializers
from . import models

class SwissProt_Serizalizer(serializers.ModelSerializer):
    class Meta:
        model = models.SwissProt_Model
        fields = '__all__'
