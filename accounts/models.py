from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        # ('visitor', 'Visiteur'),  # supprimé
        ('patient', 'Patient'),
        ('kine', 'Kinésithérapeute'),
        ('vendor', 'Vendeur'),
        ('admin', 'Administrateur'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_validated = models.BooleanField(default=True)  # True par défaut, sauf pour les kinés
    
    # Champs spécifiques aux kinésithérapeutes
    diplome = models.CharField(max_length=100, blank=True, null=True, verbose_name="Diplôme")
    wilaya = models.CharField(max_length=50, blank=True, null=True, verbose_name="Wilaya")
    diplome_file = models.ImageField(upload_to='diplomes/', blank=True, null=True, verbose_name="Photo du diplôme")

    def save(self, *args, **kwargs):
        if self.user_type == 'kine' and not self.is_validated:
            self.is_validated = False
        elif self.user_type != 'kine':
            self.is_validated = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

class Publication(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'kine'})
    texte = models.TextField()
    image = models.ImageField(upload_to='publications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur.get_full_name()} - {self.created_at:%d/%m/%Y %H:%M}"

class MessagePatientKine(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_envoyes', limit_choices_to={'user_type': 'patient'})
    kine = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_recus', limit_choices_to={'user_type': 'kine'})
    texte = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.patient.get_full_name()} à {self.kine.get_full_name()}"

class DemandePriseEnCharge(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_patient', limit_choices_to={'user_type': 'patient'})
    kine = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_kine', limit_choices_to={'user_type': 'kine'})
    lettre_medicale = models.FileField(upload_to='lettres_medicales/')
    statut = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('acceptee', 'Acceptée'), ('refusee', 'Refusée')], default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.patient.get_full_name()} à {self.kine.get_full_name()}"

class Reclamation(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    message = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    repondu = models.BooleanField(default=False)

    def __str__(self):
        return f"Réclamation de {self.patient.get_full_name()} le {self.created_at.strftime('%d/%m/%Y')}"

class Avis(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['patient', 'vendor']})
    texte = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.auteur.get_full_name()} le {self.created_at.strftime('%d/%m/%Y')}" 