from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from fitness.models import (
    AdditionalInfo,
    CustomUser,
    Diseases,
    FitnessInfo
)
from django.core.validators import RegexValidator

# Using ModelSerializer because I dont want to override the field behaviour existing in models


class RegisterSerializer(serializers.ModelSerializer):
    # Regex Validation for password
    password = serializers.CharField(
        write_only=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message=(
                    "Password must be at least 8 characters long and include "
                    "uppercase, lowercase, number, and special character."
                )
            )
        ]
    )

    class Meta:
        model = CustomUser
        # fields to serialize
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


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseases
        # fields to serialize
        fields = ['id', 'name', 'level', 'duration']

    def create(self, validated_data):
        disease = Diseases.objects.create(
            user=validated_data['user'],
            name=validated_data['name'],
            level=validated_data['level'],
            duration=validated_data['duration'],
        )
        return disease


class UserInfoSerializer(serializers.ModelSerializer):
    disease_detail = DiseaseSerializer(source="diseases", read_only=True)

    class Meta:
        model = AdditionalInfo
        # fields to serialize
        fields = [
            'diseases',
            'disease_detail',
            'smoking',
            'drinking',
            'injuries',
            'stress_level'
        ]


class FitnessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessInfo
        # fields to serialize
        fields = [
            'fitness_goal',
            'current_fitness_level',
            'workout_location',
        ]
