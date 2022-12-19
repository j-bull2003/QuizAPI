from django.urls import path

from accounts.api.v1.views import (
    UserListAPIView,
    LoginAPIView,
    SignUpAPIView
)

app_name = 'accounts-api-v1'
urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users-list'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', SignUpAPIView.as_view(), name='signup'),
]
