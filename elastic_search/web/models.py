from django.db import models

# Create your models here.
class All_info(models.Model):
    title = models.CharField('标题',max_length=125)
    tags = models.CharField('标签',max_length=32)
    url = models.URLField(verbose_name='url')
    img_url = models.URLField(verbose_name='图片url')
    summary = models.CharField(verbose_name='简介',max_length=512)


# class Word(models.Model):
#     word = models.CharField('单词',max_length=32)