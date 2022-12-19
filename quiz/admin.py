from django.contrib import admin
from quiz.models import Question, Option, Quiz


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass
