from rest_framework import serializers
from fitness.models import (
    CustomUser
)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'email',
            'age',
            'gender',
            'contact',
            'height',
            'weight',
            'diet_preference']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            age=validated_data['age'],
            gender=validated_data['gender'],
            height=validated_data['height'],
            contact=validated_data['contact'],
            weight=validated_data['weight'],
            diet_preference=validated_data['diet_preference'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
