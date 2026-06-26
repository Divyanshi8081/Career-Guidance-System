from django.db import models
from django.conf import settings

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('interest', 'Interest'),
        ('skill', 'Skill'),
        ('personality', 'Personality'),
        ('value', 'Work Value'),
    ]
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"[{self.category}] {self.text[:60]}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=300)
    weight = models.JSONField(default=dict)

    def __str__(self):
        return self.text[:60]

class AssessmentResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)
    scores = models.JSONField(default=dict)
    recommended_careers = models.JSONField(default=list)
    ai_advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

class SkillGapAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_career = models.CharField(max_length=200)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    match_percentage = models.FloatField(default=0)
    courses_suggested = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
