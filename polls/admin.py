from django.contrib import admin
from .models import Poll,Choice
# from .models import Vote


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

admin.site.register(Poll , QuestionAdmin)
admin.site.register(Choice)
# admin.site.register(Vote)

# Register your models here.
