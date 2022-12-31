from django.db import models
from core.models import AbstractTimestampModel
from django.utils.translation import gettext_lazy as _

# The 'Option' model represents a possible answer to a question in a quiz
class Option(AbstractTimestampModel):

    # 'text' is a field within 'Option'
    # 'text' is a string frield that stores the text of the option
    text = models.CharField(max_length=255)

    # 'is_correct' is a boolean field that indicates whether the option is correct to the answer
    is_correct = models.BooleanField(default=False)

    # This string method returns the text of the option when the object is printed
    def __str__(self):
        return self.text

# The 'question' model represents a quiz question (three fields)
class Question(AbstractTimestampModel):
    text = models.CharField(verbose_name=_('Text'), max_length=255)

    # 'description' is a text field that stores additional information about the question
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)

    # 'options' is a many-to-many field that stores the options for the questions
    options = models.ManyToManyField(
        verbose_name=_('Options'),
        to='quiz.Option',
        related_name='quizzes'
    )

    # This is used to define the string representation of the model 
    def __str__(self):
        return self.text

# The 'Quiz' model represents a quiz and stores data about quizzes (three fields)
class Quiz(AbstractTimestampModel):

    # 'questions' is a many-to-many field that stores the questions for the quiz'
    questions = models.ManyToManyField(
        verbose_name=_('Questions'),
        to='quiz.Question',
        related_name='quizzes'
    )

    # 'user' is a foreign key field that stores a reference to the user who took the quiz
    # The foreign key field is used to ensure that the 'Quiz' model has a reference to a valid 'User' record and;
    # allows you to easily retrieve all of the quizzes taken by a particular user by using the related_name attribute.
    user = models.ForeignKey(
        verbose_name=_('User'),

        # The 'user' field is related to the 'User' model, specified below:
        to='accounts.User',

        # This argument specifies the name of the attribute that will be used to access the related objects
        related_name='quizzes',

        # This argument specifies the action that will be taken when the referenced record is deleted
        # In this case, the CASCADE action will delete any records in the 'Quiz' model that reference the deleted 'User' record. 
        on_delete=models.CASCADE
    )

    # 'score' is an integer field that stores the score for the quiz
    score = models.IntegerField(verbose_name=_('Score'), null=True, blank=True)

