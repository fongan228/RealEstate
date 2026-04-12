from django.contrib import admin

from .models import Document, Processing, ExtractedData, Risk

admin.site.register(Document)
admin.site.register(Processing)
admin.site.register(ExtractedData)
admin.site.register(Risk)
