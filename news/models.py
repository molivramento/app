from django.db import models
from django.urls import reverse
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    category = models.CharField(max_length=50, choices=(
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('technology', 'Technology')
    ))

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class Link(models.Model):
    token = models.CharField(max_length=16)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

