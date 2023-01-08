from django.db import models


class AbstractTimestampModel(models.Model):

    # The created_date field is a DateTimeField that is set to the current date and time when an instance of the model is created.
    created_date = models.DateTimeField(auto_now_add=True)

    # The modified_date field is also a DateTimeField that is set to the current date and time every time an instance of the model is saved.
    modified_date = models.DateTimeField(auto_now=True)

    # The Meta class inside the AbstractTimestampModel class sets the abstract attribute to True, which specifies that the AbstractTimestampModel class is an abstract base class and cannot be used to create database tables. 
    class Meta:
        abstract = True

        # The ordering attribute specifies the default ordering for instances of the model, with the most recently created instances first.
        ordering = ['-id']

# In summary, this code defines an abstract base model class for a Django app that provides fields for storing the creation and modification dates of model instances and sets the default ordering for the instances.
