from rest_framework import serializers
from django.conf import settings
from account.models import Profile

class ProfileSerializer(serializers.Serializer):
    user = serializers.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=serializers.CASCADE,
    )
    position = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=1024)
    skills = serializers.CharField(max_length=500)

    def create(self, validated_data):
        """
        Create and return a new `Profile` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.position = validated_data.get('position', instance.position)
        instance.location = validated_data.get('location', instance.location)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.save()
