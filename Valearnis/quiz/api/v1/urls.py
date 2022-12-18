from django.urls import path

from quiz.api.v1.views import (
    QuestionListCreateAPIView,
    QuestionRetrieveUpdateAPIView,
    QuizListCreateAPIView,
    QuizRetrieveUpdateAPIView
)

app_name = 'quiz-api-v1'

urlpatterns = [
    path('questions/', QuestionListCreateAPIView.as_view(), name='questions-list-create'),
    path('questions/item/', QuestionRetrieveUpdateAPIView.as_view(), name='questions-retrieve-update'),

    path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list-create'),
    path('quizzes/item/', QuizRetrieveUpdateAPIView.as_view(), name='quiz-retrieve-update'),
]
