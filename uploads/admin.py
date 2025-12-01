# uploads/admin.py
from django.contrib import admin
from .models import UploadBatch

@admin.register(UploadBatch)
class UploadBatchAdmin(admin.ModelAdmin):
    list_display = ("id", "metric_type", "original_filename", "user", "created_at")
    list_filter = ("metric_type", "created_at")
    search_fields = ("original_filename", "user__username")
    readonly_fields = ("created_at", "report")
