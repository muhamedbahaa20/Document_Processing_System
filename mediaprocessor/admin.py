# admin.py

from django.contrib import admin
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file','file_name', 'file_type', 'created_at')  # Columns to display in the list view
    search_fields = ('file', 'file_type')  # Make file and file_type searchable in the admin
    list_filter = ('file_type',)  # Add a filter for file types in the admin

admin.site.register(UploadedFile, UploadedFileAdmin)