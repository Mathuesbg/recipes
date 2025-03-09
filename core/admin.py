from django.contrib import admin
from core import models

@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...