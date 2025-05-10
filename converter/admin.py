from django.contrib import admin
from .models import Tool, ToolCategory
from parler.admin import TranslatableAdmin

    
@admin.register(Tool)
class ToolsAdmin(TranslatableAdmin):
    list_display = ["name", "url", "icon", "category", "title"]


@admin.register(ToolCategory)
class ToolCategoryAdmin(TranslatableAdmin):
    list_display = ["title", "icon", "js_id"]

