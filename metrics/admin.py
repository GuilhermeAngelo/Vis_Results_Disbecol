from django.contrib import admin
from .models import MetricType, MetricRecord, UploadBatch
admin.site.register(UploadBatch)
@admin.register(MetricType)
class MetricTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "unit", "target_value", "better_when")
    list_editable = ("target_value", "better_when")
    search_fields = ("name", "code")

@admin.register(MetricRecord)
class MetricRecordAdmin(admin.ModelAdmin):
    list_display = ("metric_type", "collaborator", "date", "value", "source_batch")
    list_filter = ("metric_type", "date")
    search_fields = ("collaborator__nome", "collaborator__colaborador_id")