from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile = Profile(
            username=validated_data['username'],
            email=validated_data['email']
        )
        profile.set_password(validated_data['password'])
        profile.save()
        return profile
