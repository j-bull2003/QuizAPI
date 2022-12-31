from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from project_quiz.settings import env, MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

# The api_url_patterns variable is a tuple that contains a list of path objects and a string. 
# The list of path objects defines URL patterns for an API and maps each URL pattern to a view function or another set of URL patterns.
api_url_patterns = (
    [
        path('accounts/v1/', include('accounts.api.v1.urls')),
        path('quiz/v1/', include('quiz.api.v1.urls')),
    ], 'api'
)

# The urlpatterns list is a list of path objects that define the URL patterns for the application. 
# The first path object in the list maps the URL path '/admin/' to the Django admin site. 
# The second path object in the list maps the URL path '/api/' to the list of API URL patterns defined in the api_url_patterns variable.
urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('api/', include(api_url_patterns)),
]

# This checks the value of the ENV_TYPE environment variable and, if it is 'DEVELOPMENT', adds URL patterns for serving static files and enabling the Django Debug Toolbar.
if env.str('ENV_TYPE') == 'DEVELOPMENT':
    import debug_toolbar

    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# In summary, this code defines a list of URL patterns for a Django application and maps each URL pattern to a view function or another set of URL patterns, including an API and optional support for serving static files and enabling the Django Debug Toolbar in development.
