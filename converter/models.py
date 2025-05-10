from django.db import models
from parler.models import TranslatableModel, TranslatedFields   

class ToolCategory(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=264, blank=True, null=True)
    )
    icon = models.CharField(max_length=1000, blank=True, null=True)
    js_id = models.CharField(max_length=1000, blank=True, null=True)

class Tool(TranslatableModel):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    translations = TranslatedFields(
        name = models.CharField(max_length=264),
        title = models.CharField(max_length=264)
    )
    url = models.CharField(max_length=264)
    icon = models.CharField(max_length=264)
    category = models.ForeignKey(ToolCategory, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=2,
                                    choices=Status.choices,
                                    default=Status.DRAFT)

