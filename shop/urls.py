from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/products/', views.vendor_product_list, name='vendor_product_list'),
    path('vendeur/produits/', views.vendor_product_list, name='vendor_product_list_alt'),
    path('vendeur/produits/ajouter/', views.product_create, name='vendor_product_create'),
    path('vendeur/produit/<int:produit_id>/modifier-prix/', views.modifier_prix, name='modifier_prix'),
    path('vendeur/produit/<int:produit_id>/commandes/', views.voir_commandes_produit, name='voir_commandes_produit'),
    path('vendeur/produit/<int:produit_id>/supprimer/', views.supprimer_produit, name='supprimer_produit'),
    path('vendeur/produit/<int:produit_id>/modifier/', views.vendor_product_edit, name='vendor_product_edit'),
] 