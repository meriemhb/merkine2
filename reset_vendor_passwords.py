from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

CustomUser = get_user_model()

# Liste des comptes vendeurs à réinitialiser
vendor_accounts = [
    {'email': 'mimi.samo@outlook.fr', 'username': 'mimi.samo'},
    {'email': 'ghanoo@gmail.com', 'username': 'ghanoo'}
]

# Nouveau mot de passe pour tous les comptes
new_password = 'Vendeur123!'

for account in vendor_accounts:
    try:
        user = CustomUser.objects.get(email=account['email'])
        user.password = make_password(new_password)
        user.save()
        print(f"Mot de passe réinitialisé pour {account['email']}")
    except CustomUser.DoesNotExist:
        print(f"Compte non trouvé : {account['email']}") 