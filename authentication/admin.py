from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, Role, RolePermission

admin.site.site_header = "Authentication Admin"
admin.site.site_title = "Authentication Admin Portal"
admin.site.index_title = "Welcome to the Authentication Admin Portal"
admin.site.enable_nav_sidebar = False
admin.site.site_url = None  # Disable the admin site URL to prevent redirection
admin.site.empty_value_display = "N/A"  # Display 'N/A' for empty
admin.site.default_permissions = ()  # Disable default permissions
admin.site.has_permission = (
    lambda request: request.user.is_authenticated
)  # Ensure only authenticated users can access the admin site

admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(Role)
admin.site.register(RolePermission)
