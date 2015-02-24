from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    solved = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    want = models.IntegerField(default=0)

    class Meta:
        db_table = 'questions'

class WantListen(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question)
    user_id = models.ForeignKey(User)

    class Meta:
        db_table = 'want_listen'
