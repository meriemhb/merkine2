import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from blog.models import Article

def update_article_slugs():
    articles = Article.objects.all()
    for article in articles:
        if not article.slug:
            article.slug = slugify(article.title)
            article.save()
    
    print("Slugs des articles mis à jour avec succès!")

if __name__ == '__main__':
    update_article_slugs() 