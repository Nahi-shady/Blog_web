from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class PublishedManager(models.Manager):
    # Return all published posts in reverse chronological order (newest first).
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.status.PUBLISHED)
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DR', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    published = PublishedManager()
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]

    def __str__(self):
        return self.title
