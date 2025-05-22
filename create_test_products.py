import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindom.settings')
django.setup()

from shop.models import Product

def create_test_products():
    products = [
        {
            'name': 'Couscous Royal',
            'description': 'Un délicieux couscous traditionnel avec légumes et viandes variées.',
            'price': Decimal('2500.00'),
            'stock': 10
        },
        {
            'name': 'Chorba Frik',
            'description': 'Soupe traditionnelle algérienne au blé vert et légumes.',
            'price': Decimal('800.00'),
            'stock': 15
        },
        {
            'name': 'Merguez Maison',
            'description': 'Saucisses traditionnelles épicées, préparées selon la recette familiale.',
            'price': Decimal('1800.00'),
            'stock': 20
        },
        {
            'name': 'Tajine de Poulet',
            'description': 'Tajine de poulet aux olives et citron confit.',
            'price': Decimal('2200.00'),
            'stock': 12
        },
        {
            'name': 'Baklava',
            'description': 'Pâtisserie traditionnelle aux amandes et miel.',
            'price': Decimal('1200.00'),
            'stock': 25
        }
    ]
    
    for product_data in products:
        Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
    
    print("Produits de test créés avec succès!")

if __name__ == '__main__':
    create_test_products() 