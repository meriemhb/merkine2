from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from allauth.account.views import LoginView
from .models import CustomUser, DemandePriseEnCharge, Reclamation, Avis
from .forms import CustomUserChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from shop.models import Product
from blog.models import Article
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import VendorSignUpForm

def home(request):
    """Vue pour la page d'accueil"""
    return render(request, 'accounts/home.html')

@login_required
def profile(request):
    """Vue pour afficher le profil de l'utilisateur"""
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    """Vue pour modifier le profil de l'utilisateur"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    """Vue pour supprimer le profil de l'utilisateur"""
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('home')
    return render(request, 'accounts/delete_profile.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'patient':
            return reverse('accounts:patient_dashboard')
        elif user.user_type == 'kine':
            return reverse('accounts:profile')
        elif user.user_type == 'vendor':
            return reverse('shop:vendor_dashboard')
        return super().get_success_url()

    def form_valid(self, form):
        user = form.user
        # Si c'est un kiné, il doit être validé
        if user.user_type == 'kine' and not user.is_validated:
            messages.error(self.request, "Votre compte kiné doit être validé par un administrateur avant de pouvoir vous connecter.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Identifiants invalides. Veuillez vérifier votre email et votre mot de passe.")
        return super().form_invalid(form)

@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_users': CustomUser.objects.exclude(user_type='admin').count(),
        'total_kines': CustomUser.objects.filter(user_type='kine').count(),
        'total_patients': CustomUser.objects.filter(user_type='patient').count(),
        'total_vendors': CustomUser.objects.filter(user_type='vendor').count(),
    }
    latest_users = CustomUser.objects.exclude(user_type='admin').order_by('-date_joined')[:5]
    return render(request, 'admin_custom/dashboard.html', {'stats': stats, 'latest_users': latest_users})

@staff_member_required
def admin_users(request):
    users = CustomUser.objects.exclude(user_type='admin')
    return render(request, 'admin_custom/users.html', {'users': users})

@staff_member_required
def admin_user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.user_type != 'admin':
        user.delete()
    return redirect(reverse('accounts:admin_users'))

@staff_member_required
def admin_stats(request):
    stats = {
        'total_users': CustomUser.objects.exclude(user_type='admin').count(),
        'total_kines': CustomUser.objects.filter(user_type='kine').count(),
        'total_patients': CustomUser.objects.filter(user_type='patient').count(),
        'total_vendors': CustomUser.objects.filter(user_type='vendor').count(),
    }
    return render(request, 'admin_custom/stats.html', {'stats': stats})

# Décorateur pour accès patient uniquement
def patient_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.user_type == 'patient', login_url='/accounts/login/')(view_func))
    return decorated_view_func

@patient_required
def patient_dashboard(request):
    return render(request, 'patients/dashboard.html')

@patient_required
def kine_publications(request):
    articles = Article.objects.filter(author__user_type='kine').order_by('-created_at')
    return render(request, 'patients/kine_publications.html', {'articles': articles})

@patient_required
def patient_message_kine(request):
    kines = CustomUser.objects.filter(user_type='kine', is_active=True, is_validated=True)
    if request.method == 'POST':
        # À compléter : enregistrement du message
        messages.success(request, 'Votre message a été envoyé au kiné.')
    return render(request, 'patients/message_kine.html', {'kines': kines})

@patient_required
def patient_shop(request):
    products = Product.objects.all()
    return render(request, 'patients/shop.html', {'products': products})

@patient_required
def search_kine(request):
    kines = CustomUser.objects.filter(user_type='kine', is_active=True, is_validated=True)
    query = request.GET.get('q')
    if query:
        kines = kines.filter(first_name__icontains=query) | kines.filter(last_name__icontains=query)
    return render(request, 'patients/search_kine.html', {'kines': kines})

@patient_required
def demande_prise_en_charge(request, kine_id):
    kine = CustomUser.objects.get(id=kine_id, user_type='kine')
    # À compléter : enregistrement de la demande
    messages.success(request, f'Demande envoyée à {kine.get_full_name()}')
    return redirect('accounts:search_kine')

@patient_required
def demande_prise_en_charge_form(request):
    kine_id = request.GET.get('kine_id')
    if not kine_id:
        messages.error(request, "Veuillez sélectionner un kiné.")
        return redirect('accounts:search_kine')
        
    kine = get_object_or_404(CustomUser, id=kine_id, user_type='kine', is_active=True, is_validated=True)
    
    if request.method == 'POST':
        lettre = request.FILES.get('lettre_medicale')
        if lettre:
            # Créer la demande de prise en charge
            DemandePriseEnCharge.objects.create(
                patient=request.user,
                kine=kine,
                lettre_medicale=lettre
            )
            messages.success(request, "Demande envoyée avec succès !")
            return redirect('accounts:search_kine')
        else:
            messages.error(request, "Veuillez joindre une lettre médicale.")
            
    return render(request, 'patients/demande_prise_en_charge_form.html', {'kine': kine})

def kine_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.user_type == 'kine', login_url='/accounts/login/')(view_func))
    return decorated_view_func

@kine_required
def kine_dashboard(request):
    return render(request, 'kine/dashboard.html')

@kine_required
def kine_publications_manage(request):
    # Affichage + formulaire de publication (texte, image)
    # À compléter avec logique de création
    return render(request, 'kine/publications.html')

@kine_required
def kine_messages(request):
    # Liste des messages reçus, possibilité de répondre
    return render(request, 'kine/messages.html')

@kine_required
def kine_demandes(request):
    # Liste des demandes de prise en charge, accepter/refuser
    return render(request, 'kine/demandes.html')

@kine_required
def kine_profile(request):
    # Affichage/modification du profil kiné
    return render(request, 'kine/profile.html')

def signup_kine(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'kine'
            user.is_validated = False  # ou True selon ta politique
            user.save()
            return redirect('account_login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup_kine.html', {'form': form})

def signup_vendor(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Votre compte vendeur a été créé avec succès!')
            return redirect('account_login')
    else:
        form = VendorSignUpForm()
    return render(request, 'accounts/signup_vendor.html', {'form': form}) 

@login_required
def profile_vendor(request):
    if request.user.user_type != 'vendor':
        return redirect('accounts:home')
    return render(request, 'accounts/profile_vendor.html')

@patient_required
def reclamation_form(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Reclamation.objects.create(patient=request.user, message=message)
            messages.success(request, "Votre réclamation a été envoyée à l'administrateur.")
            return redirect('accounts:patient_dashboard')
        else:
            messages.error(request, "Veuillez écrire votre réclamation.")
    return render(request, 'patients/reclamation_form.html')

@staff_member_required
def admin_reclamations(request):
    if request.method == 'POST':
        reclamation_id = request.POST.get('reclamation_id')
        reponse = request.POST.get('reponse')
        reclamation = Reclamation.objects.get(id=reclamation_id)
        reclamation.reponse = reponse
        reclamation.repondu = True
        reclamation.save()
        messages.success(request, "Réponse envoyée au patient.")
    reclamations = Reclamation.objects.all().order_by('-created_at')
    return render(request, 'admin_custom/reclamations.html', {'reclamations': reclamations})

@login_required
def avis_site(request):
    if request.user.user_type not in ['patient', 'vendor']:
        return redirect('accounts:home')
    if request.method == 'POST':
        texte = request.POST.get('texte')
        if texte:
            Avis.objects.create(auteur=request.user, texte=texte)
            messages.success(request, "Merci pour votre avis !")
            return redirect('accounts:avis_site')
        else:
            messages.error(request, "Veuillez écrire un avis.")
    avis_list = Avis.objects.all().order_by('-created_at')
    return render(request, 'avis/avis_site.html', {'avis_list': avis_list}) 