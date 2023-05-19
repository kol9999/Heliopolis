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
from django.urls import path
from api.students.views import  RegisterStudent, TestAPIView
from api.instructor.views import RegisterInstructor
from api.common.views import Login, OtpValidation


urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test_api_view'),
    #student registration
    path('register-student/', RegisterStudent.as_view(), name='register_student'),
    #instructor registration
    path('register-instructor/', RegisterInstructor.as_view(), name='register_instructor'),
    #token validation
    path('token-validation/', OtpValidation.as_view(), name='token-validation'),
    #login
    path('login/', Login.as_view(), name = 'login')
]
