import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import CustomUser

def test_login(email, password):
    """Teste la connexion avec les identifiants fournis"""
    user = authenticate(email=email, password=password)
    if user is not None:
        print(f"Connexion réussie pour {email}")
        print(f"Type d'utilisateur : {user.user_type}")
        print(f"Nom d'utilisateur : {user.username}")
        print(f"Prénom : {user.first_name}")
        print(f"Nom : {user.last_name}")
        return True
    else:
        print(f"Échec de la connexion pour {email}")
        return False

# Test avec les comptes vendeurs
vendor_accounts = [
    {'email': 'mimi.samo@outlook.fr', 'password': 'Vendeur123!'},
    {'email': 'ghanoo@gmail.com', 'password': 'Vendeur123!'}
]

print("Test de connexion avec les comptes vendeurs :")
print("-" * 50)

for account in vendor_accounts:
    print(f"\nTest avec {account['email']} :")
    test_login(account['email'], account['password'])
    print("-" * 50) 