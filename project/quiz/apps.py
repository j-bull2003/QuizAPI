from django.apps import AppConfig

# This code defines a configuration class for a Django app that specifies the default field for auto-incrementing primary keys and the name of the app.
class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'
