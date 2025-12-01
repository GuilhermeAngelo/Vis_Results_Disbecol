from django.contrib.auth.decorators import login_required, user_passes_test  # ou permission_required
from django.shortcuts import render, redirect
from django.contrib import messages

from metrics.models import MetricType
from .services import import_xlsx

@login_required
@user_passes_test(lambda u: u.is_staff)  # ou @permission_required('uploads.can_upload_metrics', raise_exception=True)
def upload_csv(request):
    metric_types = MetricType.objects.all().order_by("name")

    if request.method == "POST":
        metric_id = request.POST.get("metric_type")
        file = request.FILES.get("file")

        if not metric_id or not file:
            messages.error(request, "Selecione a métrica e o arquivo.")
            return render(request, "uploads/upload.html", {"metric_types": metric_types})

        try:
            metric = MetricType.objects.get(pk=metric_id)
        except MetricType.DoesNotExist:
            messages.error(request, "Métrica inválida.")
            return render(request, "uploads/upload.html", {"metric_types": metric_types})

        fname = (file.name or "").lower()
        if not (fname.endswith(".xlsx") or fname.endswith(".xls")):
            messages.error(request, "Envie um arquivo Excel (.xlsx ou .xls).")
            return render(request, "uploads/upload.html", {"metric_types": metric_types})

        ok, report = import_xlsx(metric, file, request.user)
        if ok:
            messages.success(request, f"Importação concluída. Linhas importadas: {report.get('imported', 0)}.")
        else:
            msg = report.get("error") or f"Falhas: {len(report.get('errors', []))}"
            messages.error(request, f"Falha no import: {msg}")

        return redirect("uploads:upload")  # << nome/namespace corretos

    return render(request, "uploads/upload.html", {"metric_types": metric_types})
