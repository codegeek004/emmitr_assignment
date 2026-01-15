from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from fitness.models import (
    AdditionalInfo,
    CustomUser,
    Diseases,
    FitnessInfo
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


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diseases
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
        fields = [
            'fitness_goal',
            'current_fitness_level',
            'workout_location',
        ]
