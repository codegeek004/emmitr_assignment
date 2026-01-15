from django.db import models
from django.contrib.auth.models import AbstractUser
# for implementing uuids in primary key so that no one can predict ids based on sequential numbers
import uuid

# CustomUser model overriding the default user model to add some custom fields


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.IntegerField()
    # Using Choices for the input field to accept only 3 types of values in the field
    GENDER_CHOICES = (
        ('M', 'male'),
        ('F', 'female'),
        ('OTHERS', 'prefer not to say')
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES)
    # using BigIntegerField because IntegerField does not support big numbers
    contact = models.BigIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    # Using choices for the input field to accept only 4 types of values in the field
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
    # Foreign Key referenced with CustomUser model
    user = models.ForeignKey('fitness.CustomUser', on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=20)
    # Using choices for the input field to accept only 3 types of values in the field
    LOCATION_CHOICES = (
        ('home', 'Home'),
        ('gym', 'Gym'),
        ('outdoor', 'Outdoor')
    )
    # Using choices for the input field to accept only 3 types of values in the field
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
    # Foreign Key referenced with CustomUser model
    user = models.ForeignKey(
        'fitness.CustomUser', on_delete=models.CASCADE)
    # Foreign Key referenced with Disease model
    diseases = models.ForeignKey(
        'fitness.Diseases', on_delete=models.SET_NULL, null=True, blank=True)
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    injuries = models.TextField(blank=True)
    # Using choices for the input field to accept only 3 types of values in the field
    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    stress_level = models.CharField(
        max_length=6, choices=LEVEL_CHOICES, default='low')


class Diseases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Foreign Key referenced with Disease model
    user = models.ForeignKey('fitness.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    # Using choices for the input field to accept only 3 types of values in the field
    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    level = models.CharField(
        max_length=6, choices=LEVEL_CHOICES, default='low')
    duration = models.IntegerField()
