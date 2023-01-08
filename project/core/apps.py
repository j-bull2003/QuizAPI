from django.apps import AppConfig

# The CoreConfig class sets the default_auto_field attribute to specify the default field that should be used for auto-incrementing primary keys in the models of the app, and the name attribute to specify the name of the app.
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

# In summary, this code defines a configuration class for a Django app that specifies the default field for auto-incrementing primary keys and the name of the app.
