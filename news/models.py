from django.db import models
from django.urls import reverse
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=(
        ('politics', 'Politics'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('technology', 'Technology')
    ))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])