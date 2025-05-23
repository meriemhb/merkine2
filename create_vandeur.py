import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

def create_vandeur_account():
    User = get_user_model()
    # Créer le compte visiteur s'il n'existe pas
    vandeur, created = User.objects.get_or_create(
        email='vandeur@kindom.com',
        defaults={
            'username': 'vandeur',
            'first_name': 'Vandeur',
            'last_name': 'Kindom',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False
        }
    )
    
    if created:
        vandeur.set_password('vandeur123')
        vandeur.save()
        print("Compte vandeur créé avec succès!")
        print("Email: vandeur@kindom.com")
        print("Mot de passe: vandeur123")
    else:
        print("Le compte vandeur existe déjà.")

def create_vendor_account():
    User = get_user_model()
    
    # Créer le compte vendeur s'il n'existe pas
    vendor, created = User.objects.get_or_create(
        email='vendor@kindom.com',
        defaults={
            'username': 'vendor',
            'first_name': 'Vendeur',
            'last_name': 'Kindom',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'user_type': 'vendor'
        }
    )
    
    if created:
        vendor.set_password('vendor123')
        vendor.save()
        print("Compte vendeur créé avec succès!")
        print("Email: vendor@kindom.com")
        print("Mot de passe: vendor123")
    else:
        print("Le compte vendeur existe déjà.")

if __name__ == '__main__':
    create_vendor_account() 