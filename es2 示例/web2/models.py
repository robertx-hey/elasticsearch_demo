from django.db import models

# Create your models here.

# class Blog(models.Model):
#     title = models.CharField(max_length=)


class Article(models.Model):
    title = models.CharField(max_length=512)
    summary = models.CharField(max_length=512)
    a_url = models.URLField()
    img_url = models.URLField()
    tags = models.CharField(max_length=128)