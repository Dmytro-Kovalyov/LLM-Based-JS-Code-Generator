from rest_framework import serializers

class GenerateRequestSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=500)
    test_parameters = serializers.ListField(allow_empty=True)

class TestRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parameters = serializers.ListField(allow_empty=True)