
from rest_framework import viewsets
from api.course.serializers import (ChapterSerializer, CourseSerializer, EnrollmentSerializer,
    LessonSerializer, CourseSerializerForAuthenticate)
from rest_framework.permissions import IsAuthenticated
from apps.course.models import Chapter, Course, Enrollment, Lesson
from rest_framework.exceptions import PermissionDenied
import rest_framework.views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import serializers


class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "post"]
    # queryset = Course.objects.select_related('category', 'owner').all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user).select_related('category', 'owner').order_by('-id')

    def perform_update(self, serializer):
        # Retrieve the current user
        user = self.request.user
        course = serializer.instance
        if user.pk == course.owner.pk:
            serializer.save()
        else:
            # User does not have permission to edit the course
            raise PermissionDenied("You do not have permission to edit this course.")


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    http_method_names = ['post']
    queryset = Enrollment.objects.select_related('course', 'student').all()

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']

        try:
            course_obj = Course.objects.values('active').get(pk = course.pk)
            if not course_obj['active']:
                raise ValidationError('Inactive course can\'t enroll')
        except:
            raise ValidationError('Course not found')
        enroll_obj = Enrollment.objects.filter(course=course, student=user).exists()
        if enroll_obj:
            raise serializers.ValidationError('Already enrolled')
        serializer.save(student=user)


class CoursePublicViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    http_method_names = ["get"]


    def get_serializer_class(self):
        user = self.request.user
        if user:
            return CourseSerializerForAuthenticate
        return self.serializer_class

    def get_queryset(self):
        return Course.objects.filter(active=True).select_related('category', 'owner').order_by('-updated_at')

class ChapterViewSet(viewsets.ModelViewSet):

    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "post"]
    # queryset = Course.objects.select_related('category', 'owner').all()

    def get_queryset(self):
        user = self.request.user
        return Chapter.objects.filter(course__owner=user).select_related('course')

    def perform_update(self, serializer):
        # Retrieve the current user
        user = self.request.user
        chapter = serializer.instance
        if user.pk == chapter.course.owner.pk:
            serializer.save()
        else:
            # User does not have permission to edit the course
            raise PermissionDenied("You do not have permission to edit this course.")


class LessonViewSet(viewsets.ModelViewSet):

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "post"]
    # queryset = Course.objects.select_related('category', 'owner').all()

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(chapter__course__owner=user).select_related('chapter')

    def perform_update(self, serializer):
        # Retrieve the current user
        user = self.request.user
        lesson = serializer.instance
        if user.pk == lesson.chapter.course.owner.pk:
            serializer.save()
        else:
            # User does not have permission to edit the course
            raise PermissionDenied("You do not have permission to edit this course.")


class CourseDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        course_id = request.query_params.get('course_id')
        user = request.user
        print(user)
        is_his_course = Course.objects.filter(owner = user).exists()
        if not is_his_course:
            return Response({'message': 'Permission not allowed'}, status=status.HTTP_403_FORBIDDEN,)
        if course_id:

            course_obj = get_object_or_404(Course, id=course_id)
            data = {
                'title' : course_obj.title,
                'description' : course_obj.description,
                'chapters' : []
            }

            chapters = Chapter.objects.filter(course = course_obj)

            if chapters:

                for chapter in chapters:
                    chapter_data = {
                        'id': chapter.pk,
                        'chapter_title': chapter.title,
                        'lessons': []
                    }
                    lessons = Lesson.objects.filter(chapter=chapter)
                    for lesson in lessons:
                        lesson_data = {
                            'id': lesson.pk,
                            'lesson_title': lesson.title,
                            'lesson_video': f'http://127.0.0.1:8000{lesson.video.url}' if lesson.video else None,
                            'lesson_image': lesson.image.url if lesson.image else None,
                            'lesson_type':lesson.type
                        }

                        chapter_data['lessons'].append(lesson_data)

                    data['chapters'].append(chapter_data)
            return Response(data)

        return Response({'message': '?course_id needed'}, status=status.HTTP_400_BAD_REQUEST,)


class CourseDetailsAfterEnrollment(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        course_id = request.query_params.get('course_id')
        user = request.user
        is_he_enroll = Enrollment.objects.filter(course=course_id, student=user).exists()

        if not is_he_enroll:
            return Response({'message': 'Permission not allowed'}, status=status.HTTP_403_FORBIDDEN,)
        if course_id:

            course_obj = get_object_or_404(Course, id=course_id)
            data = {
                'title' : course_obj.title,
                'description' : course_obj.description,
                'chapters' : []
            }

            chapters = Chapter.objects.filter(course = course_obj)

            if chapters:

                for chapter in chapters:
                    chapter_data = {
                        'id': chapter.pk,
                        'chapter_title': chapter.title,
                        'lessons': []
                    }
                    lessons = Lesson.objects.filter(chapter=chapter)
                    for lesson in lessons:
                        lesson_data = {
                            'id': lesson.pk,
                            'lesson_title': lesson.title,
                            'lesson_video': f'http://127.0.0.1:8000{lesson.video.url}' if lesson.video else None,
                            'lesson_image': lesson.image.url if lesson.image else None,
                            'lesson_type':lesson.type
                        }

                        chapter_data['lessons'].append(lesson_data)

                    data['chapters'].append(chapter_data)
            return Response(data)

        return Response({'message': '?course_id needed'}, status=status.HTTP_400_BAD_REQUEST,)
