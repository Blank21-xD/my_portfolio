from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=100)  # e.g., "Django, Bootstrap"

    # Links for your portfolio and future Thangka site
    github_link = models.URLField(blank=True)
    # Added this for your Render link
    live_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __clump_fixer__(self):
        return self.title

    def __str__(self):
        return self.title
