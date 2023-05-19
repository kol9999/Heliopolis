from django.db import models
from apps.common.models import CustomUser, TimeStampAndVisibility
from django.contrib.auth.models import AbstractUser, Group
from apps.common.models import CustomUser
# Create your models here.

class Student(CustomUser):

    def save(self, *args, **kwargs):
        # Call the parent class's save() method
        super().save(*args, **kwargs)
        if not self.groups.filter(name='student').exists():
        # Get or create the desired group
            group, created = Group.objects.get_or_create(name='student')

            # Add the user to the group
            self.groups.add(group)
