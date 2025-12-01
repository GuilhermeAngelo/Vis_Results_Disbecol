from datetime import date, timedelta, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Avg, Count, Q

from accounts.models import Collaborator
from metrics.models import MetricType, MetricRecord


def _parse_date_param(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def _looks_like_time_metric(m: MetricType) -> bool:
    code = (m.code or "").lower()
    unit = (m.unit or "").lower()
    name = (m.name or "").lower()
    hints = ("time", "tempo", "hh:mm", "hhmm", "ti", "duracao", "duração", "sla")
    unit_hints = ("min", "minuto", "minutos", "hora", "horas", "h")
    return any(h in code for h in hints) or any(h in name for h in hints) or any(u in unit for u in unit_hints)


def _group_key_for_metric(m: MetricType) -> str:
    import unicodedata
    def norm(s: str) -> str:
        s = (s or "").lower()
        s = unicodedata.normalize("NFD", s)
        return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    name = norm(m.name); code = norm(m.code)
    if ("aderencia" in name and "raio" in name) or ("aderencia" in code and "raio" in code):
        return "bonus"
    if ("aderencia" in name and "checklist" in name) or ("aderencia" in code and "checklist" in code):
        return "bonus"
    if ("producao" in name) or ("producao" in code):
        return "rv"
    if ("devolucao" in name) or ("devolucao" in code):
        return "rv"
    return "ics_ivs"


@login_required
def my_dashboard(request):
    # garante colaborador
    collab, created = Collaborator.objects.get_or_create(
        user=request.user,
        defaults={
            "colaborador_id": f"U{request.user.id}",
            "nome": request.user.get_full_name() or request.user.get_username(),
            "equipe": "",
        },
    )
    if created:
        messages.info(request, "Criamos seu cadastro de colaborador automaticamente.")

    # Filtro de datas
    start = _parse_date_param(request.GET.get("start"))
    end = _parse_date_param(request.GET.get("end"))
    if not start and not end:
        end = date.today()
        start = end - timedelta(days=29)
    if start and end and start > end:
        start, end = end, start

    base_q = MetricRecord.objects.filter(collaborator=collab)
    if start:
        base_q = base_q.filter(date__gte=start)
    if end:
        base_q = base_q.filter(date__lte=end)

    # Séries, metadados e grupos
    series = {}
    meta = {}
    by_group = {"bonus": [], "rv": [], "ics_ivs": []}
    all_metrics = list(MetricType.objects.all().order_by("name"))

    for m in all_metrics:
        qs = base_q.filter(metric_type=m).order_by("date")
        series[m.code] = list(qs.values("date", "value"))
        meta[m.code] = {
            "name": m.name,
            "unit": m.unit or "",
            "is_time": _looks_like_time_metric(m),
            "target_value": m.target_value,
            "better_when": m.better_when,
        }
        by_group[_group_key_for_metric(m)].append(m.code)

    # Média e contagem (ignora zeros)
    self_stats_qs = (
        base_q.values("metric_type__code")
        .annotate(
            media=Avg("value", filter=Q(value__gt=0)),
            n=Count("id", filter=Q(value__gt=0)),
        )
    )
    self_stats = {
        row["metric_type__code"]: {"avg": row["media"], "count": row["n"]}
        for row in self_stats_qs
    }

    # Dias fora da meta por métrica (ignora zeros)
    fail_days = {}  # {code: ["YYYY-MM-DD", ...]}
    for m in all_metrics:
        code = m.code
        t = m.target_value
        if t is None:
            fail_days[code] = []
            continue
        cond = Q(value__gt=0)
        if m.better_when == "higher":
            cond &= Q(value__lt=t)
        else:  # lower
            cond &= Q(value__gt=t)
        days_qs = (
            base_q.filter(metric_type=m)
                  .filter(cond)
                  .order_by("date")
                  .values_list("date", flat=True)
        )
        fail_days[code] = [d.isoformat() for d in days_qs]

    # Códigos com qualquer dia fora da meta
    unmet_codes = [c for c, days in fail_days.items() if days]
    # Ou média fora da meta também conta:
    for m in all_metrics:
        code = m.code
        if code in unmet_codes:
            continue
        t = m.target_value
        if t is None:
            continue
        stat = self_stats.get(code)
        avg = stat["avg"] if stat else None
        if avg is None:
            continue
        if (m.better_when == "higher" and avg < t) or (m.better_when == "lower" and avg > t):
            unmet_codes.append(code)

    unmet_names = [m.name for m in all_metrics if m.code in unmet_codes]
    has_unmet = bool(unmet_codes)
    forms_url = getattr(settings, "MS_FORMS_URL", "")

    sections = [
        {"key": "bonus", "title": "Bônus", "codes": by_group["bonus"]},
        {"key": "rv", "title": "Remuneração Variável", "codes": by_group["rv"]},
        {"key": "ics_ivs", "title": "ICS e IVS", "codes": by_group["ics_ivs"]},
    ]

    return render(
        request,
        "dashboards/my_dashboard.html",
        {
            "collab": collab,
            "series": series,
            "meta": meta,
            "self_stats": self_stats,
            "sections": sections,
            "start": start.isoformat() if start else "",
            "end": end.isoformat() if end else "",
            "forms_url": forms_url,
            "has_unmet": has_unmet,
            "unmet_codes": unmet_codes,
            "unmet_names": unmet_names,
            "fail_days": fail_days,  # << NOVO: dias fora da meta por métrica
        },
    )
