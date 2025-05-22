import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Article

User = get_user_model()

def create_test_articles():
    # Créer un utilisateur de test si nécessaire
    admin_user, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()

    articles = [
        {
            'title': 'Bienvenue sur notre blog',
            'content': '''Nous sommes ravis de vous accueillir sur notre blog. Ici, vous trouverez des articles intéressants sur divers sujets.
            
            Notre mission est de partager des connaissances et des expériences qui enrichiront votre vie quotidienne.
            
            N'hésitez pas à explorer nos articles et à nous laisser vos commentaires !''',
            'author': admin_user,
            'published': True
        },
        {
            'title': 'Les dernières tendances',
            'content': '''Découvrez les dernières tendances dans notre domaine. Nous analysons les nouveautés et vous les présentons de manière claire et concise.
            
            Restez à jour avec les dernières innovations et les meilleures pratiques.''',
            'author': admin_user,
            'published': True
        },
        {
            'title': 'Conseils et astuces',
            'content': '''Voici quelques conseils et astuces pour vous aider dans votre quotidien. Ces informations sont basées sur notre expérience et nos recherches.
            
            Nous espérons que ces conseils vous seront utiles !''',
            'author': admin_user,
            'published': True
        }
    ]
    
    for article_data in articles:
        Article.objects.get_or_create(
            title=article_data['title'],
            defaults=article_data
        )
    
    print("Articles de test créés avec succès!")

if __name__ == '__main__':
    create_test_articles() 