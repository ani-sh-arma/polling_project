from django import forms
from .models import Poll


class addPoll(forms.ModelForm):
    options = forms.CharField(
        max_length=255,
        required=True,
        help_text="Enter poll options separated by commas (e.g., Option 1, Option 2, Option 3)",
    )

    class Meta:
        model = Poll
        fields = ["question"]
