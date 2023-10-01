from django import forms
from .models import Poll

class addPoll(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'option5']
