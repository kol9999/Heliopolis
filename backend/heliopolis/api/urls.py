"""
URL configuration for heliopolis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from api.students.views import RegisterStudent, TestAPIView
from api.instructor.views import RegisterInstructor
from api.common.views import Login, OtpValidation
from rest_framework import routers
from api.course.views import (ChapterViewSet, CourseDetails, CoursePublicViewSet, CourseViewSet,
    EnrollmentViewSet, LessonViewSet, ReviewAndRetingViewSet)
from api.course.views import CourseDetailsAfterEnrollment


router = routers.DefaultRouter()

router.register('course', CourseViewSet, basename="course")
router.register('chapter', ChapterViewSet, basename="chapter")
router.register('lesson', LessonViewSet, basename="lesson")
router.register('enrollment', EnrollmentViewSet, basename="enrollment")
router.register('review_rating', ReviewAndRetingViewSet, basename="review_rating")



###public view
router.register('course_public_view', CoursePublicViewSet, basename='course_public_view'),


urlpatterns = [
    path('', include(router.urls)),
    path('test/', TestAPIView.as_view(), name='test_api_view'),
    # course details
    path('course_details/', CourseDetails.as_view(), name="course details"),
    #details after enrollment
    path('course-details-after-enrollment/', CourseDetailsAfterEnrollment.as_view(), name="course-details-after-enrollment"),
    # student registration
    path('register-student/', RegisterStudent.as_view(), name='register_student'),
    # instructor registration
    path('register-instructor/', RegisterInstructor.as_view(), name='register_instructor'),
    # token validation
    path('token-validation/', OtpValidation.as_view(), name='token-validation'),
    # login
    path('login/', Login.as_view(), name='login')
]
