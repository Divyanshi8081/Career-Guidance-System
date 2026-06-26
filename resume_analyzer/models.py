from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255, blank=True)
    extracted_text = models.TextField(blank=True)
    skills_found = models.JSONField(default=list)
    experience_years = models.FloatField(null=True, blank=True)
    education_level = models.CharField(max_length=100, blank=True)
    ats_score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    word_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.username} - {self.original_filename}"

    def get_ats_color(self):
        if self.ats_score >= 80:
            return 'success'
        elif self.ats_score >= 60:
            return 'warning'
        return 'danger'

    def get_ats_label(self):
        if self.ats_score >= 80:
            return 'Excellent'
        elif self.ats_score >= 60:
            return 'Good'
        elif self.ats_score >= 40:
            return 'Fair'
        return 'Needs Work'
