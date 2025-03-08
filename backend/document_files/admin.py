from django.contrib import admin
from document_files.models import Document
# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin)