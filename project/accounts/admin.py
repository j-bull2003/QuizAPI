from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from accounts.models import User

# The '@admin.register' decorator is used to register the UserAdmin class with the Django admin interface.
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # The 'list_display' attribute of the 'UserAdmin' class specifies which fields of the 'User' model should be displayed in the list view of the Django admin interface.
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    
    # The 'fieldsets' attribute specifies how the fields of the 'User' model should be organized in the form used to create and update 'User' objects in the Django admin interface. 
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [_('Personal info'), {'fields': ['first_name', 'last_name', 'email']}],
        [_('Permissions'), {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}],
    ]

    # The date_hierarchy attribute specifies the field that should be used to provide date-based navigation in the list view of the Django admin interface.
    date_hierarchy = 'date_joined'

# The admin.site.register function is used to register the Permission model with the Django admin interface. 
# This allows you to manage Permission objects in the Django admin interface.
admin.site.register(Permission)