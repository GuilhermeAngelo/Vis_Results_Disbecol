from django.db import models
from accounts.models import Collaborator


class MetricType(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=60, unique=True)
    unit = models.CharField(max_length=20, blank=True, default="")
    # --- NOVOS CAMPOS:
    target_value = models.FloatField(null=True, blank=True)
    BETTER_CHOICES = [
        ("higher", "Quanto maior, melhor"),
        ("lower", "Quanto menor, melhor"),
    ]
    better_when = models.CharField(
        max_length=10,
        choices=BETTER_CHOICES,
        default="higher",
    )

    def __str__(self):
        return f"{self.name}"


class UploadBatch(models.Model):
    metric_type = models.ForeignKey(MetricType, on_delete=models.PROTECT)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=16, default="pending") # pending, imported, failed
    report = models.JSONField(default=dict, blank=True)


class MetricRecord(models.Model):
    collaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE, db_index=True)
    metric_type = models.ForeignKey(MetricType, on_delete=models.PROTECT)
    date = models.DateField(db_index=True)
    value = models.DecimalField(max_digits=14, decimal_places=4)
    source_batch = models.ForeignKey(
        'uploads.UploadBatch',               # <— note a string com app.model
        on_delete=models.PROTECT,
        related_name='records',
    )


class Meta:
    unique_together = ("collaborator", "metric_type", "date")
    indexes = [models.Index(fields=["metric_type", "date"])]