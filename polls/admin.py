from django.contrib import admin
from .models import Poll,Choice , Voted
# from .models import Vote



class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['option_text', 'question', 'votes']

    
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields":["question","creator"]}),
        ("Date information", {"fields":["pub_date"],"classes":["collapse"]}),
    ]
    inlines = [ChoiceInLine]
    list_display = ["question", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question"]


class VotedAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll' , 'choice', 'voted']


admin.site.register(Poll , QuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(Voted , VotedAdmin)

