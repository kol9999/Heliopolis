from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.students.serializers import StudentCreateSerializer
from apps.otp.models import Otp
from django.db import transaction


from rest_framework.authtoken.models import Token
from apps.student.models import Student
from apps.instructor.models import Instructor

class TestAPIView(APIView):
    def get(self, request):
        data = {
            'message': 'This is a test API view.',
            'status': 'success'
        }
        return JsonResponse(data)

class RegisterStudent(APIView):
    def post(self, request):
        data = request.data
        serializer = StudentCreateSerializer(data = data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                email = serializer.validated_data['email']
                otp = Otp.create_otp(email)
                return Response({'message': "Successfully register, please validate token"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST,)


