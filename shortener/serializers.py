from rest_framework import serializers


class CreateURLSerializer(serializers.Serializer):
    url = serializers.URLField()


class URLResponseSerializer(serializers.Serializer):
    original_url = serializers.URLField()
    hash = serializers.CharField()
