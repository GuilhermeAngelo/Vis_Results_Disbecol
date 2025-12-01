# dashboards/templatetags/dash_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(d, key):
    try:
        return d.get(key)
    except Exception:
        return None

@register.filter
def minutes_to_hms(value):
    """
    Converte minutos (float) para 'HH:MM:SS'.
    Ex.: 90.5 -> '01:30:30'
    """
    try:
        minutes = float(value)
    except (TypeError, ValueError):
        return ""
    total_seconds = int(round(minutes * 60))
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
