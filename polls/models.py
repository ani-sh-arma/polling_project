import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone

class Poll(models.Model):
    question = models.CharField(max_length=255)
    creator =  models.ForeignKey(User, on_delete=models.CASCADE)
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
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text
    

class Voted(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

    # obj = Choice()

    def __str__(self):
        return self.choice.option_text
    