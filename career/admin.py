from django.contrib import admin
from .models import Question, Option, AssessmentResult, SkillGapAnalysis

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'category', 'order']
    list_filter = ['category']
    inlines = [OptionInline]

@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']

@admin.register(SkillGapAnalysis)
class SkillGapAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_career', 'match_percentage', 'created_at']
