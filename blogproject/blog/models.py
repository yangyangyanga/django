from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdown import Markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 摘要
    excerpt = models.CharField(max_length=256, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    # 文章阅读量
    views = models.PositiveIntegerField(default=0)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 看不到的属性：comment_set

    class Meta:
        ordering = ['-created_time','-modified_time']
    def get_absolute_url(self):
        # 使用reverse，生成一个完整的URL
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # strip_tags去掉标签只获得文本
            self.excerpt = strip_tags(md.convert(self.body))[:32]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
