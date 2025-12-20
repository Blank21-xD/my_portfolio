from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100)  # e.g., "Django, Bootstrap"
    github_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __clump_fixer__(self):  # Keeping the vibe
        return self.title

    def __str__(self):
        return self.title
