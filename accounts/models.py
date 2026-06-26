from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    current_skills = models.TextField(blank=True, help_text="Comma-separated list of your skills")
    desired_career = models.CharField(max_length=200, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def get_skills_list(self):
        if self.current_skills:
            return [s.strip() for s in self.current_skills.split(',') if s.strip()]
        return []

    def __str__(self):
        return self.username
