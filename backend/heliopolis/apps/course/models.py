from django.db import models
from apps.common.models import CustomUser, TimeStampAndVisibility
from django.db.models import SET_NULL
from django.utils.text import slugify
from apps.instructor.models import Instructor

# Create your models here.


class Category(TimeStampAndVisibility):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(TimeStampAndVisibility):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_owner')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Chapter(TimeStampAndVisibility):
    title = models.CharField(max_length=255)

    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(TimeStampAndVisibility):
    TYPE_CHOICES = [
        (1, 'Content'),
        (2, 'Quiz'),
        (3, 'Assignment'),
    ]
    chapter = models.ForeignKey('Chapter', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    
    video = models.TextField()
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=1, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)  # thumbnail

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Quiz(TimeStampAndVisibility):
    section = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField()
    correct_ans = models.IntegerField()
    options = models.JSONField()


class Attachment(TimeStampAndVisibility):
    section = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='attachment')
