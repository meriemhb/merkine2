import os
import django
import sys

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from blog.models import Article, Comment
from shop.models import Product
from appointments.models import Appointment
from accounts.models import CustomUser

def delete_content():
    try:
        # Supprimer les articles du blog
        articles = Article.objects.all()
        articles_count = articles.count()
        articles.delete()
        print(f"{articles_count} articles supprimés")

        # Supprimer les commentaires
        comments = Comment.objects.all()
        comments_count = comments.count()
        comments.delete()
        print(f"{comments_count} commentaires supprimés")

        # Supprimer les produits de la boutique
        products = Product.objects.all()
        products_count = products.count()
        products.delete()
        print(f"{products_count} produits supprimés")

        # Supprimer les rendez-vous
        appointments = Appointment.objects.all()
        appointments_count = appointments.count()
        appointments.delete()
        print(f"{appointments_count} rendez-vous supprimés")

        # Réinitialiser les informations des utilisateurs (sauf admin)
        users = CustomUser.objects.exclude(user_type='admin')
        for user in users:
            user.phone_number = ''
            user.address = ''
            user.profile_picture = None
            user.bio = ''
            user.save()
        print(f"Informations de {users.count()} utilisateurs réinitialisées")

        print("\nSuppression terminée avec succès!")

    except Exception as e:
        print(f"Erreur lors de la suppression: {str(e)}")

if __name__ == '__main__':
    delete_content() 