from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResetPasswordToken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    password = models.CharField(max_length=64)
    token = models.CharField(max_length=64)

    class Meta:
        db_table = 'reset_password_token'