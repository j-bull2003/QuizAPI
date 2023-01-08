from django.urls import path

# This code defines a list of URL patterns for a Django application and maps each URL pattern to a view function. 
# The app_name variable specifies the name of the application. 
# The urlpatterns list is a list of path objects that define the URL patterns for the application.

from accounts.api.v1.views import (
    UserListAPIView,
    LoginAPIView,
    SignUpAPIView
)

# The first path object in the list maps the URL path '/users/' to the UserListAPIView view. 
# The second path object in the list maps the URL path '/login/' to the LoginAPIView view. 
# The third path object in the list maps the URL path '/register/' to the SignUpAPIView view.

app_name = 'accounts-api-v1'
urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users-list'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', SignUpAPIView.as_view(), name='signup'),
]

# In summary, this code defines a list of URL patterns for a Django application and maps each URL pattern to a view function.
