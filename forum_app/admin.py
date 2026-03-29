from django.contrib import admin
from .models import Question, Answer, Like


class QuestionAdmin(admin.ModelAdmin):
     list_display = ('id', 'title')

class AnswerAdmin(admin.ModelAdmin):
     pass

class LikeAdmin(admin.ModelAdmin):
     pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Like, LikeAdmin)