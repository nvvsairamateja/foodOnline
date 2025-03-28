from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Customizing the Django admin panel for the User model


class CustomAdmin(UserAdmin):
    # Fields that will be displayed in the list view of the admin panel
    list_display = ["username", "email", "role", "is_active"]

    # Default ordering of users in the admin panel (latest joined users first)
    ordering = ("-date_joined",)

    # Horizontal filters (used for many-to-many fields, not needed here)
    filter_horizontal = ()

    # Filters for the right sidebar in the admin panel (empty for now)
    list_filter = ()

    # Fieldsets define the layout of the user edit form in the admin panel (empty for now)
    fieldsets = ()


# Register the User model with the custom admin class
admin.site.register(User, CustomAdmin)
admin.site.register(UserProfile)