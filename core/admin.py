from django.contrib import admin
from core import models

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'is_published', "created_at"]
    list_display_links = ['title', "created_at"]
    search_fields = ['id', "title", 'description', 'author', "slug", "preparation_steps"]
    list_filter = ['category', "author", "is_published", "preparation_steps_is_html"]
    list_per_page = 10
    list_editable = ["is_published"]
    ordering = '-id',
    prepopulated_fields= {"slug" : ("title",)}

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...