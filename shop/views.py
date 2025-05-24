from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Order, OrderItem
from django import forms
from django.forms import ModelForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category', 'description', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'style': 'font-size:1.1rem; padding:0.7rem 1rem; border-radius:8px; background:#f8fafc; border:1.5px solid #b6c6e3;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs['rows'] = 5
            if field.widget.__class__.__name__ == 'ClearableFileInput':
                field.widget.attrs['class'] = 'form-control mt-2 w-100'
            else:
                field.widget.attrs['class'] = 'form-control w-100'
            field.widget.attrs['style'] = 'max-width: 100%; min-width: 350px; font-size: 1.1rem; padding: 0.7rem 1rem;'

class ProductPriceForm(ModelForm):
    class Meta:
        model = Product
        fields = ['price']
        labels = {'price': 'Nouveau prix'}

def product_list(request):
    """Vue pour lister les produits"""
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})
@login_required
def product_create(request):
    """View to allow vendors to add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user  # Assuming the Product model has a vendor field
            product.save()
            return redirect('shop:vendor_product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/vendor/product_form.html', {'form': form})

def product_detail(request, pk):
    """Vue pour afficher les détails d'un produit"""
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews
    })

@login_required
def cart_detail(request):
    """Vue pour afficher le panier"""
    return render(request, 'shop/cart_detail.html')

@login_required
def cart_add(request, product_id):
    """Vue pour ajouter un produit au panier"""
    product = get_object_or_404(Product, id=product_id)
    # Logique d'ajout au panier
    messages.success(request, f'{product.name} a été ajouté au panier.')
    return redirect('shop:cart_detail')

@login_required
def cart_remove(request, product_id):
    """Vue pour retirer un produit du panier"""
    product = get_object_or_404(Product, id=product_id)
    # Logique de suppression du panier
    messages.success(request, f'{product.name} a été retiré du panier.')
    return redirect('shop:cart_detail')

@login_required
def checkout(request):
    """Vue pour le processus de paiement"""
    if request.method == 'POST':
        # Logique de paiement
        pass
    return render(request, 'shop/checkout.html')

@login_required
def order_list(request):
    """Vue pour lister les commandes"""
    if request.user.user_type in ['patient', 'kine']:
        orders = Order.objects.filter(customer=request.user)
    else:
        orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    """Vue pour afficher les détails d'une commande"""
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'shop/order_detail.html', {'order': order})

def vendor_required(view_func):
    return login_required(user_passes_test(lambda u: u.user_type == 'vendor')(view_func))

@vendor_required
def vendor_dashboard(request):
    # Récupérer les produits du vendeur
    products = Product.objects.filter(vendor=request.user)
    
    # Récupérer les commandes contenant ces produits
    order_items = OrderItem.objects.filter(product__in=products)
    orders = Order.objects.filter(items__in=order_items).distinct()
    
    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'shop/vendor/dashboard.html', context) 

@vendor_required
def vendor_product_list(request):
    products = Product.objects.filter(vendor=request.user)
    return render(request, 'shop/vendor/product_list.html', {'products': products})

@vendor_required
def modifier_prix(request, produit_id):
    produit = get_object_or_404(Product, id=produit_id, vendor=request.user)
    if request.method == 'POST':
        form = ProductPriceForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prix modifié avec succès.')
            return redirect('shop:vendor_product_list')
    else:
        form = ProductPriceForm(instance=produit)
    return render(request, 'shop/vendor/modifier_prix.html', {'form': form, 'produit': produit})

@vendor_required
def voir_commandes_produit(request, produit_id):
    produit = get_object_or_404(Product, id=produit_id, vendor=request.user)
    commandes = OrderItem.objects.filter(product=produit)
    return render(request, 'shop/vendor/commandes_produit.html', {'commandes': commandes, 'produit': produit})

@vendor_required
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Product, id=produit_id, vendor=request.user)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès.')
        return redirect('shop:vendor_product_list')
    return render(request, 'shop/vendor/supprimer_produit.html', {'produit': produit})

@vendor_required
def vendor_product_edit(request, produit_id):
    produit = get_object_or_404(Product, id=produit_id, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès.')
            return redirect('shop:vendor_dashboard')
    else:
        form = ProductForm(instance=produit)
    return render(request, 'shop/vendor/product_form.html', {'form': form, 'produit': produit})