from django.urls import path
from fitness.views import (
    DiseaseView,
    HomeView,
    RegisterView,
    LoginView,
    UserInfoView,
    DiseaseView,
    FitnessInfoView,
    WorkoutPlanView,
    DietPlanView
)
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_info/', UserInfoView.as_view(), name='user_info'),
    path('diseases/', DiseaseView.as_view(), name='diseases'),
    path("fitness_info/", FitnessInfoView.as_view(), name='fitness'),
    path("workout_plan/", WorkoutPlanView.as_view(), name="workout-plan"),
    path('diet_plan/', DietPlanView.as_view(), name='diet_plan')


]
