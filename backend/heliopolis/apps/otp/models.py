from django.db import models
from apps.common.models import TimeStampAndVisibility

# Create your models here.
class Otp(TimeStampAndVisibility):
    email = models.EmailField(unique=True)
    attempt = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    otp = models.CharField(max_length=40, editable=False)

    def __str__(self):
        return "{} - {}".format(self.email, self.otp)

    @classmethod
    def create_otp(cls, email):
        otp_value = cls.generate_otp()
        # try:
        otp = Otp(email = email, otp = otp_value, active = True)
        otp.save()
        return True
        # except:
        #     return False

    @classmethod
    def generate_otp(cls):
        otp = 1234
        return 1234