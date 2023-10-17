import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone

class Poll(models.Model):
    question = models.CharField(max_length=255)
    creator =  models.ForeignKey(User, on_delete=models.CASCADE)
    # option1 = models.CharField(max_length=255)
    # option2 = models.CharField(max_length=255)
    # option3 = models.CharField(max_length=255)
    # option4 = models.CharField(max_length=255)
    # option5 = models.CharField(max_length=255)

    pub_date = models.DateTimeField("date published",default=timezone.now)


    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    # voter = models.ForeignKey(User,on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text

# class Vote(models.Model):
#     question = models.ForeignKey(Poll,on_delete=models.CASCADE)
#     Op1votes = models.IntegerField(default=0)
#     Op2votes = models.IntegerField(default=0)
#     Op3votes = models.IntegerField(default=0)
#     Op4votes = models.IntegerField(default=0)
#     Op5votes = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.question.question}"

# Create your models here.
