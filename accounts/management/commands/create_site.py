from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Crée le site par défaut pour django-allauth'

    def handle(self, *args, **options):
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'Kindom'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Site par défaut créé avec succès!'))
        else:
            self.stdout.write(self.style.SUCCESS('Le site par défaut existe déjà.')) 