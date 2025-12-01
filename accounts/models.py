from django.conf import settings
from django.db import models


class Collaborator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    colaborador_id = models.CharField(max_length=64, unique=True)
    nome = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255, blank=True)
    gestor_nome = models.CharField(max_length=255, blank=True)
    ativo = models.BooleanField(default=True)


def __str__(self):
    return f"{self.colaborador_id} - {self.nome}"