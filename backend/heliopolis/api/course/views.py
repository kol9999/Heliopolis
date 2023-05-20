
from rest_framework import viewsets
from api.course.serializers import ChapterSerializer, CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from apps.course.models import Chapter, Course, Lesson
from rest_framework.exceptions import PermissionDenied


class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch"]
    # queryset = Course.objects.select_related('category', 'owner').all()

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user).select_related('category', 'owner')

    def perform_update(self, serializer):
        # Retrieve the current user
        user = self.request.user
        course = serializer.instance
        if user.pk == course.owner.pk:
            serializer.save()
        else:
            # User does not have permission to edit the course
            raise PermissionDenied("You do not have permission to edit this course.")


class ChapterViewSet(viewsets.ModelViewSet):

    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch"]
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
    http_method_names = ["get", "patch"]
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
