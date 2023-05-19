from api.instructor.serializers import InstructorCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.otp.models import Otp
from django.db import transaction

class RegisterInstructor(APIView):
    def post(self, request):
        data = request.data
        serializer = InstructorCreateSerializer(data = data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                email = serializer.validated_data['email']
                otp = Otp.create_otp(email)
                return Response({'message': "Successfully register, please validate token"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST,)