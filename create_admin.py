import os
import django
import sys

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

def create_admin():
    # Création de l'administrateur
    admin_username = 'admin'
    admin_email = 'admin@kineedom.com'
    admin_password = 'Admin@123'  # Mot de passe sécurisé

    try:
        # Vérifier si l'administrateur existe déjà
        if not CustomUser.objects.filter(username=admin_username).exists():
            admin = CustomUser.objects.create(
                username=admin_username,
                email=admin_email,
                password=make_password(admin_password),
                is_superuser=True,
                is_staff=True,
                is_active=True,
                user_type='admin'  # Ajout du type d'utilisateur
            )
            print(f"Administrateur créé avec succès!")
            print(f"Nom d'utilisateur: {admin_username}")
            print(f"Email: {admin_email}")
            print(f"Mot de passe: {admin_password}")
        else:
            print("L'administrateur existe déjà!")
    except Exception as e:
        print(f"Erreur lors de la création de l'administrateur: {str(e)}")

if __name__ == '__main__':
    create_admin() 