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


class OtpValidation(APIView):
    def post(self, request):
        data = request.data
        try:
            email = request.data['email']
        except:
            return Response({'message': 'email needed'}, status=status.HTTP_400_BAD_REQUEST,)
        try:
            otp = request.data['otp']
        except:
            return Response({'message': 'otp needed'}, status=status.HTTP_400_BAD_REQUEST,)

        # try:
        otp_object = Otp.objects.get(email = email)
        if otp_object.otp == otp:
            user = Student.objects.get(email = email)
            token = Token.objects.get_or_create(user = user)[0]
            data = {
                "email":email,
                "token":str(token)
            }
            print(token)
            return Response({"status":"successfully validate",'message': data})
        return Response({'message': "Otp not match"})

