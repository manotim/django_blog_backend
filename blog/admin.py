from django.contrib import admin
from .models import Category, News, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'category', 'author', 'date_posted', 'is_breaking']
    list_filter = ['category', 'is_breaking', 'date_posted']
    search_fields = ['title', 'body']


admin.site.register(Comment)
admin.site.register(Like)
