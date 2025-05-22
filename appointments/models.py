from django.db import models
from django.conf import settings

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    )
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    kine = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kine_appointments')
    date = models.DateTimeField()
    duration = models.IntegerField(help_text='Durée en minutes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"RDV: {self.patient} avec {self.kine} le {self.date}" 