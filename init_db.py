import os
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

def create_test_users():
    User = get_user_model()
    
    # Créer un compte patient
    patient, created = User.objects.get_or_create(
        email='patient@kindom.com',
        defaults={
            'username': 'patient',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'is_active': True,
            'user_type': 'patient',
            'phone_number': '0612345678',
            'address': '123 Rue de Paris, 75001 Paris'
        }
    )
    if created:
        patient.set_password('patient123')
        patient.save()
        print("Compte patient créé avec succès!")
    
    # Créer un compte kiné
    kine, created = User.objects.get_or_create(
        email='kine@kindom.com',
        defaults={
            'username': 'kine',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'is_active': True,
            'user_type': 'kine',
            'phone_number': '0623456789',
            'address': '456 Avenue des Kinés, 75002 Paris',
            'bio': 'Kinésithérapeute spécialisée en rééducation sportive'
        }
    )
    if created:
        kine.set_password('kine123')
        kine.save()
        print("Compte kiné créé avec succès!")

def create_visitor_account():
    User = get_user_model()
    
    # Créer le compte visiteur s'il n'existe pas
    visitor, created = User.objects.get_or_create(
        email='visitor@kindom.com',
        defaults={
            'username': 'visitor',
            'first_name': 'Visiteur',
            'last_name': 'Kindom',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'visitor'
        }
    )
    
    if created:
        visitor.set_password('visitor123')
        visitor.save()
        print("Compte visiteur créé avec succès!")
        print("Email: visitor@kindom.com")
        print("Mot de passe: visitor123")
    else:
        print("Le compte visiteur existe déjà.")

def init_db():
    # Appliquer toutes les migrations
    call_command('migrate')
    
    # Créer le site par défaut
    from django.contrib.sites.models import Site
    Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Kindom'
        }
    )
    
    # Créer les comptes de test
    create_visitor_account()
    create_test_users()
    
    print("Base de données initialisée avec succès!")

if __name__ == '__main__':
    init_db() 