from django.contrib import admin
from apps.course.models import Chapter, Course, Lesson

# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)

