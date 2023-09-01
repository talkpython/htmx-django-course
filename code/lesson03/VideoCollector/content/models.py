# VideoCollector/content/models.py
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    image_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = [
            "name",
        ]

    def __str__(self):
        return f"Category(name={self.name})"

    def __len__(self):
        return Video.objects.filter(categories=self).count()


class Video(models.Model):
    youtube_id = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50, blank=True, default="")
    view_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"Video(title={self.title})"
