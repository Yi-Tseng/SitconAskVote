from django.db import models

# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    solved = models.IntegerField()
    author = models.IntegerField()

    class Meta:
        db_table = 'questions'