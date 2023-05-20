from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
# Create your models here.
class TimeStampAndVisibility(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    alias = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    
    email = models.EmailField(verbose_name='Email Address', unique=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_student')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def get_user_group(self, *args, **kwargs):
        return self.groups.all()