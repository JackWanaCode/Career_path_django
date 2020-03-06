from rest_framework import serializers
from job.models import JobDb

class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    company = serializers.CharField(max_length=40)
    location = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=100)
    description = serializers.CharField()
    link = serializers.CharField(max_length=5000)
    date_post = serializers.IntegerField()
    html_description = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `JobDb` instance, given the validated data.
        """
        return JobDb.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `JobDb` instance, given the validated data.
        """
        instance.company = validated_data.get('company', instance.company)
        instance.location = validated_data.get('location', instance.location)
        instance.position = validated_data.get('position', instance.position)
        instance.description = validated_data.get('description', instance.description)
        instance.link = validated_data.get('link', instance.link)
        instance.date_post = validated_data.get('date_post', instance.date_post)
        instance.html_description = validated_data.get('html_description', instance.html_description)
        instance.save()
