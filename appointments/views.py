from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment

@login_required
def appointment_list(request):
    """Vue pour lister les rendez-vous"""
    if request.user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.user_type == 'kine':
        appointments = Appointment.objects.filter(kine=request.user)
    else:
        appointments = Appointment.objects.none()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    """Vue pour créer un rendez-vous"""
    if request.method == 'POST':
        # Logique de création du rendez-vous
        pass
    return render(request, 'appointments/appointment_form.html')

@login_required
def appointment_detail(request, pk):
    """Vue pour afficher les détails d'un rendez-vous"""
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    """Vue pour modifier un rendez-vous"""
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        # Logique de mise à jour du rendez-vous
        pass
    return render(request, 'appointments/appointment_form.html', {'appointment': appointment})

@login_required
def appointment_delete(request, pk):
    """Vue pour supprimer un rendez-vous"""
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Le rendez-vous a été supprimé avec succès.')
        return redirect('appointments:list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment}) 