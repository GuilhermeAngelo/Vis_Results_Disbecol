# uploads/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from metrics.models import MetricType

User = get_user_model()

class UploadBatch(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="upload_batches"
    )
    metric_type = models.ForeignKey(
        MetricType, on_delete=models.CASCADE, related_name="upload_batches"
    )
    original_filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    # relatório do import: {"imported": n, "created": n, "updated": n, "errors":[...]}
    report = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_upload_metrics", "Can upload metrics XLS/XLSX files"),
        ]

    def __str__(self) -> str:
        who = self.user.get_username() if self.user else "system"
        return f"{self.metric_type} · {self.original_filename} · {who} · {self.created_at:%Y-%m-%d %H:%M}"
