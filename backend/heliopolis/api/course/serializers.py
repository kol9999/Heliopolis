from rest_framework import serializers
from apps.course.models import Chapter, Course, Enrollment, Lesson, ReviewAndRating
from apps.common.models import CustomUser

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = '__all__'

class CourseSerializerForAuthenticate(serializers.ModelSerializer):
    enroll_status = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Course
        fields = '__all__'

    def get_enroll_status(self, obj):
        request = self.context.get('request')
        user = request.user if request and not request.user.is_anonymous else None
        print(user)
        enroll_obj = Enrollment.objects.filter(student=user, course=obj).exists()
        if enroll_obj:
            return True
        return False


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class CourseReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewAndRating
        fields = '__all__'
    
    def to_representation(self, instance):
        # Customize the representation of the serialized object
        representation = super().to_representation(instance)
        try:
            user = CustomUser.objects.get(pk = instance.student.pk)
            representation['student'] = user.email
            return representation
        except:
        # Modify the 'representation' dictionary as needed
        
            return representation

