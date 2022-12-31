from django.contrib.auth.models import AbstractUser

# This code defines a model class for a Django app. 
# The User class is a subclass of AbstractUser, which is a class provided by Django that defines a basic user model. 
# The User class does not define any additional fields or methods, so it simply inherits all the fields and methods of the AbstractUser class.

class User(AbstractUser):
    pass
