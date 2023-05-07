from rest_framework import serializers
from .models import Script

class ScriptListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Script
        fields = ["id", "function_name"]