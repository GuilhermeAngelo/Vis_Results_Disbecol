from django.contrib import admin
from .models import Collaborator
@admin.register(Collaborator)
class CAdmin(admin.ModelAdmin):
    list_display = ("colaborador_id", "nome", "equipe", "ativo")
    search_fields = ("colaborador_id", "nome", "equipe")