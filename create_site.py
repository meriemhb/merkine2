from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

def create_default_site():
    # Créer le site par défaut
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Kindom'
        }
    )
    if created:
        print("Site par défaut créé avec succès!")
    else:
        print("Le site par défaut existe déjà.") 