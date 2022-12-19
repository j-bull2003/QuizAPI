from django.db import models
from core.models import AbstractTimestampModel
from django.utils.translation import gettext_lazy as _


class Option(AbstractTimestampModel):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Question(AbstractTimestampModel):
    text = models.CharField(verbose_name=_('Text'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    options = models.ManyToManyField(
        verbose_name=_('Options'),
        to='quiz.Option',
        related_name='quizzes'
    )

    def __str__(self):
        return self.text


class Quiz(AbstractTimestampModel):
    questions = models.ManyToManyField(
        verbose_name=_('Questions'),
        to='quiz.Question',
        related_name='quizzes'
    )
    user = models.ForeignKey(
        verbose_name=_('User'),
        to='accounts.User',
        related_name='quizzes',
        on_delete=models.CASCADE
    )
    score = models.IntegerField(verbose_name=_('Score'), null=True, blank=True)

