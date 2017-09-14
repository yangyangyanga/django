from django import template
from django.db.models.aggregates import Count

from ..models import Post,Category, Tag

register = template.Library()

# 最新文章模板标签
@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all()[:num]

# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
# 分类模板标签
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)








