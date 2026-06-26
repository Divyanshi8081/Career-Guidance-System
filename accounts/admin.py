from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'desired_career']
    fieldsets = UserAdmin.fieldsets + (
        ('Career Info', {'fields': ('bio', 'profile_pic', 'current_skills', 'desired_career',
                                    'linkedin_url', 'github_url', 'experience_years')}),
    )
