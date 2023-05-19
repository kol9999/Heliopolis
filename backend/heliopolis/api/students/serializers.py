import django.db
from rest_framework import serializers
from apps.student.models import Student

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'email', 'password'
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user