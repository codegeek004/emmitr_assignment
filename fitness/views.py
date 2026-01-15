from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from fitness.models import (
    AdditionalInfo,
    FitnessInfo,
    Diseases
)
from fitness.text_to_speech import text_to_speech
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
import requests
import json
from decouple import config
# jwt
from rest_framework_simplejwt.tokens import RefreshToken


class HomeView(APIView):
    def get(self, request):

        return Response(
            {
                "message": "Welcome to the API",
            })


# View for register endpoint


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


# View for login endpoint


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user is not None:
                # generates jwt access token and refresh token
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


# view for disease endpoint


class DiseaseView(APIView):
    # check if the user is authenticated
    permission_classes = [IsAuthenticated]

    def get(self, request):
        diseases = Diseases.objects.filter(user=request.user)
        # returns multiple objects if there are any
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DiseaseSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(user=request.user)
            return Response(
                {"message": "Disease Added Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        disease_id = request.data.get('id')
        if not disease_id:
            return Response(
                {"error": "ID required"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            disease = Diseases.objects.get(id=disease_id, user=request.user)
            disease.delete()
            return Response({"message": "Deleted"}, status=status.HTTP_200_OK)
        except Diseases.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# view for user_info endpoint
# uses builtin mixins with GenericAPIView for get, post, put and patch methods


class UserInfoView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    # fetch the database objects (model: AdditionalInfo)
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


# view for fitness_info endpoint
# uses builtin mixins with GenericAPIView for get, post, put and patch methods


class FitnessInfoView(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    serializer_class = FitnessInfoSerializer
    # checks if the user is authenticated
    permission_classes = [IsAuthenticated]

    # fetch the database objects (model: FitnessInfo)
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


# view for workout_plan endpoint


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
            "Do NOT include explanations, markdown, or code blocks."
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

        prompt = f"""
        Generate a personalized 7-day workout plan.

        User context:
        {json.dumps(user_context, indent=2)}

        Rules:
        - Output MUST be valid raw JSON.
        - Do NOT use markdown.
        - Do NOT use code blocks.
        - Start immediately with "{{".
        - Follow this schema exactly:
        {schema}
        - Be practical, safe, and realistic.
        - Reduce intensity if stress, injury, or disease exists.
        """
        # calling groq api with headers
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config('OPENAI_API_KEY', cast=str)}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 700,
            },
            timeout=30,
        )

        response.raise_for_status()
        # output of the llm
        raw_output = response.json()["choices"][0]["message"]["content"]

        try:
            # converts the output of the api(response from llm) to json
            workout_plan = json.loads(raw_output)
            # calls the text_to_speech function on jsonified output
            voice_response = (
                text_to_speech(json.dumps(workout_plan))
                if workout_plan else None
            )

        except json.JSONDecodeError:
            return Response(
                {
                    "error": "AI returned invalid JSON",
                    "raw_response": raw_output,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "workout_plan": workout_plan,
                "voice_response": voice_response,
            },
            status=status.HTTP_200_OK,
        )


# view for diet_plan endpoint


class DietPlanView(APIView):
    # checks if the user is authenticated
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
            "Do NOT include explanations, markdown, or code blocks."
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

        prompt = f"""
        Generate a personalized 7-day Indian diet plan.

        User context:
        {json.dumps(user_context, indent=2)}

        Rules:
        - Output MUST be valid raw JSON.
        - Do NOT use markdown.
        - Do NOT use code blocks.
        - Start immediately with "{{".
        - Follow this schema exactly:
        {schema}
        - Be practical, safe, and realistic.
        - Reduce intensity if stress, injury, or disease exists.
        """
        # calls the api with prompt defined above
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config('OPENAI_API_KEY', cast=str)}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 700,
            },
            timeout=30,
        )

        response.raise_for_status()
        # output from the api(response from llm)
        raw_output = response.json()["choices"][0]["message"]["content"]

        try:
            # converts the response from llm to json
            diet_plan = json.loads(raw_output)
            # calls the text_to_speech function and passes jsonified output as parameter
            voice_response = (
                text_to_speech(json.dumps(diet_plan))
                if diet_plan else None
            )

        except json.JSONDecodeError:
            return Response(
                {
                    "error": "AI returned invalid JSON",
                    "raw_response": raw_output,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "diet_plan": diet_plan,
                "voice_response": voice_response,
            },
            status=status.HTTP_200_OK,
        )
