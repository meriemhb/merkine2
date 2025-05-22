import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

def create_kine():
    username = 'kine1'
    email = 'kine1@kineedom.com'
    password = 'Kine@123'
    user = CustomUser.objects.filter(username=username).first()
    if not user:
        CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            user_type='kine',
            is_active=True,
            is_staff=False
        )
        print("Compte kiné créé avec succès !")
        print(f"Identifiant : {username}")
        print(f"Email : {email}")
        print(f"Mot de passe : {password}")
    else:
        user.email = email
        user.password = make_password(password)
        user.user_type = 'kine'
        user.is_active = True
        user.is_staff = False
        user.save()
        print("Compte kiné mis à jour et réinitialisé !")
        print(f"Identifiant : {username}")
        print(f"Email : {email}")
        print(f"Mot de passe : {password}")

if __name__ == '__main__':
    create_kine() 