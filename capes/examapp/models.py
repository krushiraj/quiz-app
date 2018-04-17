from django.db import models
from django.db.models import Field as _Field
from django.contrib.auth.models import User
import uuid

USER_ID_LENGTH = 15

# Create your models here.
#Create a table for instructor and student. Each inst can conduct any no. of exams and each stud can take any no. of exams
#
class Evaluated(models.Model):
    id = models.IntegerField(primary_key= True)