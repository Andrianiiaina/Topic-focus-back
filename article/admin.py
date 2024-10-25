from django.contrib import admin
from .models import Publication
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display=('title', 'file', 'link', 'content', 'extra', 'category')
