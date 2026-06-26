from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'original_filename', 'ats_score', 'education_level', 'uploaded_at']
    list_filter = ['education_level', 'uploaded_at']
    readonly_fields = ['extracted_text', 'skills_found']
