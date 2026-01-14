from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('M', 'male'),
        ('F', 'female'),
        ('OTHERS', 'prefer not to say')
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES)
    contact = models.BigIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    DIET_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto')
    )
    diet_preference = models.CharField(
        max_length=14, choices=DIET_CHOICES, default='veg')


class FitnessInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('fitness.CustomUser', on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=20)
    LOCATION_CHOICES = (
        ('home', 'Home'),
        ('gym', 'Gym'),
        ('outdoor', 'Outdoor')
    )
    FITNESS_LEVEL = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    )
    current_fitness_level = models.CharField(
        max_length=12, choices=FITNESS_LEVEL, default='beginner')
    workout_location = models.CharField(
        max_length=50, choices=LOCATION_CHOICES, default='home')


class AdditionalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diseases = models.ForeignKey('fitness.Diseases', on_delete=models.CASCADE)
    family_history = models.ForeignKey(
        'fitness.FamilyHistory', on_delete=models.CASCADE)
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    injuries = models.TextField(blank=True)
    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    stress_level = models.CharField(
        max_length=6, choices=LEVEL_CHOICES, default='low')


class FamilyHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    level = models.CharField(
        max_length=6, choices=LEVEL_CHOICES, default='low')


class Diseases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    level = models.CharField(
        max_length=6, choices=LEVEL_CHOICES, default='low')
    duration = models.IntegerField()
