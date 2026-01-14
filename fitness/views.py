from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from fitness.models import AdditionalInfo, FitnessInfo
from fitness.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserInfoSerializer,
    DiseaseSerializer,
    FitnessInfoSerializer
)
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from django.conf import settings
import requests
import json
# jwt
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken


class HomeView(APIView):
    def get(self, request):
        response_text = '''Motivational Lines

        Consistency beats intensity when intensity fades.

        Small actions, repeated daily, build unstoppable momentum.

        Discipline is self-respect in action.

        Progress is quiet—keep going anyway.

        Lifestyle Tips

        Sleep and wake at the same time every day
        energy follows rhythm.

        Eat protein first at meals to stabilize energy and focus.

        Move for five minutes every hour—walk, stretch, reset.

        Limit screens one hour before bed to protect deep sleep.

        Posture Tips

        Keep feet flat, hips slightly higher than knees, spine neutral.

        Screen at eye level
        elbows close to the body at 90°.

        Pull shoulders gently back and down—avoid shrugging.

        Do a 30-second chest opener every hour to counter slouching.'''
        return Response(
            {
                "message": "Welcome to the API",
                "Quotes": response_text
            })


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User Created Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response(
                    {"access_token": str(refresh.access_token),
                     "refresh_token": str(refresh)
                     }
                )
            return Response({
                "error": "Invalid Credentials"},
                status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DiseaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Disease Added Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, created = AdditionalInfo.objects.get_or_create(
            user=self.request.user
        )
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FitnessInfoView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    serializer_class = FitnessInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = FitnessInfo.objects.get_or_create(
            user=self.request.user
        )
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class WorkoutPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        fitness_info = FitnessInfo.objects.filter(user=user).first()
        additional_info = AdditionalInfo.objects.filter(user=user).first()
        disease = additional_info.diseases if additional_info and additional_info.diseases else None

        user_context = {
            "age": user.age,
            "gender": user.gender,
            "height_cm": user.height,
            "weight_kg": user.weight,
            "diet_preference": user.diet_preference,
            "fitness_goal": fitness_info.fitness_goal if fitness_info else None,
            "fitness_level": fitness_info.current_fitness_level if fitness_info else None,
            "workout_location": fitness_info.workout_location if fitness_info else None,
            "smoking": additional_info.smoking if additional_info else False,
            "drinking": additional_info.drinking if additional_info else False,
            "stress_level": additional_info.stress_level if additional_info else "low",
            "injuries": additional_info.injuries if additional_info else None,
            "disease": {
                "name": disease.name,
                "level": disease.level,
                "duration_years": disease.duration,
            } if disease else None,
        }

        system_message = (
            "You are a JSON API. "
            "Return ONLY valid JSON. "
            "Do NOT include explanations, markdown, or code."
        )

        schema = """
        {
          "overview": string,
          "weekly_plan": {
            "day_1": string,
            "day_2": string,
            "day_3": string,
            "day_4": string,
            "day_5": string,
            "day_6": string,
            "day_7": string
          },
          "safety_notes": string
        }
        """

        prompt = """
        Generate a personalized 7-day workout plan.

        Rules:
        - Output MUST be valid raw JSON.
        - Do NOT use markdown formatting.
        - Do NOT use code blocks (no ```json).
        - Start the response immediately with the character "{".
        - Follow the schema exactly.
        - Be practical, safe, and realistic.
        - Reduce intensity if stress, injury, or disease exists"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Workout Generator",
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 700,
            },
            timeout=60,
        )

        response.raise_for_status()
        raw_output = response.json()["choices"][0]["message"]["content"]

        try:
            workout_plan = json.loads(raw_output)
        except json.JSONDecodeError:
            return Response(
                {
                    "error": "AI returned invalid JSON",
                    "raw_response": raw_output
                },
                status=500
            )

        return Response(
            workout_plan,
            status=status.HTTP_200_OK
        )
