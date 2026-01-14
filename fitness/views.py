from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from fitness.serializers import (
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework import status
from django.contrib.auth import authenticate

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
