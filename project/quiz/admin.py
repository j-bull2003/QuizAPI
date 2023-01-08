from django.contrib import admin
from quiz.models import Question, Option, Quiz

# This code defines custom model admin classes for a Django app.
# The OptionAdmin, QuestionAdmin, and QuizAdmin classes are subclasses of admin.ModelAdmin, which is a class provided by Django that allows you to customize the way a model is displayed and edited in the Django admin site.

# The @admin.register decorator registers each model admin class with the Django admin site, allowing instances of the corresponding model to be displayed and edited in the Django admin site.


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

# Since each model admin class does not define any additional fields or methods, it simply inherits all the fields and methods of the admin.ModelAdmin class.
# This code defines custom model admin classes for a Django app and registers them with the Django admin site, allowing instances of the corresponding models to be displayed and edited in the Django admin site.



