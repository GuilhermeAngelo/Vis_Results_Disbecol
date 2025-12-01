from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from .models import Collaborator

def _ensure_collaborator(user):
    Collaborator.objects.get_or_create(
        user=user,
        defaults={
            "colaborador_id": f"U{user.id}",
            "nome": user.get_full_name() or user.get_username(),
            "equipe": "",
        },
    )

@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    _ensure_collaborator(user)

@receiver(user_logged_in)
def on_user_logged_in(request, user, **kwargs):
    _ensure_collaborator(user)
