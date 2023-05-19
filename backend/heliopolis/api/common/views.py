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
from apps.common.models import CustomUser



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
            try:
                user = Student.objects.get(email = email)
            except:
                user = Instructor.objects.get(email = email)
            token = Token.objects.get_or_create(user = user)[0]
            if token:
                user.is_active = True
                user.save()
            data = {
                "email":email,
                "token":str(token)
            }
            print(token)
            return Response({"status":"successfully validate",'message': data})
        return Response({'message': "Otp not match"})

class Login(APIView):
    def post(self, request):
        data = request.data
        try:
            email = request.data['email']
        except:
            return Response({'message': 'email needed'}, status=status.HTTP_400_BAD_REQUEST,)
        try:
            password = request.data['password']
        except:
            return Response({'message': 'password needed'}, status=status.HTTP_400_BAD_REQUEST,)
        try:
            user = CustomUser.objects.get(email = email)
        except:
            return Response({'message': 'wrong credential'}, status=status.HTTP_400_BAD_REQUEST,)
        if user.check_password(password):
            token = Token.objects.get_or_create(user = user)[0]
            data = {
                'message': 'Successfully logged in',
                'token': str(token)
            }
            return Response(data)
        return Response({'message': 'wrong credential'}, status=status.HTTP_400_BAD_REQUEST,)



        # try:
        # otp_object = Otp.objects.get(email = email)
        # if otp_object.otp == otp:
        #     try:
        #         user = Student.objects.get(email = email)
        #     except:
        #         user = Instructor.objects.get(email = email)
        #     token = Token.objects.get_or_create(user = user)[0]
        #     if token:
        #         user.is_active = True
        #         user.save()
        #     data = {
        #         "email":email,
        #         "token":str(token)
        #     }
        #     print(token)
        #     return Response({"status":"successfully validate",'message': data})
        # return Response({'message': "Otp not match"})