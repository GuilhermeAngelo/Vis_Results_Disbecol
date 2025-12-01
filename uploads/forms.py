from django import forms
from metrics.models import MetricType


class CsvUploadForm(forms.Form):
    metric_type = forms.ModelChoiceField(queryset=MetricType.objects.all())
    file = forms.FileField()