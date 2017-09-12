from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Post

admin.site.register(Category)
admin.site.register(Tag)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "body", "created_time", "modified_time", "excerpt", "category", "author"]
admin.site.register(Post, PostAdmin)
