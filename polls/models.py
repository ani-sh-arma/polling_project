from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    # id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    creator =  models.ForeignKey(User, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    option5 = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.creator} || {self.question}"

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voter = models.ForeignKey(User,on_delete=models.CASCADE)
    vote = models.CharField(max_length=255)

    def __str__(self):
        return self.voter.username

class Vote(models.Model):
    question = models.ForeignKey(Poll,on_delete=models.CASCADE)
    Op1votes = models.IntegerField(default=0)
    Op2votes = models.IntegerField(default=0)
    Op3votes = models.IntegerField(default=0)
    Op4votes = models.IntegerField(default=0)
    Op5votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question.question}"

# Create your models here.
