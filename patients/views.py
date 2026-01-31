from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.conf import settings
from .models import Patient, PatientDocument
from .serializers import PatientSerializer, PatientCreateSerializer, PatientDocumentSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] if settings.DEBUG else [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientSerializer
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        
        # Filtrage par recherche
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(patient_id__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filtrage par statut
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            # En mode développement, utiliser un utilisateur par défaut
            from users.models import User
            default_user = User.objects.filter(is_superuser=True).first()
            if default_user:
                serializer.save(created_by=default_user)
            else:
                serializer.save()

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    permission_classes = [AllowAny] if settings.DEBUG else [IsAuthenticated]
    serializer_class = PatientSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PatientCreateSerializer
        return PatientSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_stats_view(request):
    """Vue pour les statistiques des patients"""
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status='active').count()
    inactive_patients = Patient.objects.filter(status='inactive').count()
    
    return Response({
        'total': total_patients,
        'active': active_patients,
        'inactive': inactive_patients
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_search_view(request):
    """Vue de recherche avancée des patients"""
    query = request.query_params.get('q', '')
    
    if len(query) < 2:
        return Response({'patients': []})
    
    patients = Patient.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(patient_id__icontains=query) |
        Q(email__icontains=query) |
        Q(phone_number__icontains=query)
    )[:10]  # Limiter à 10 résultats
    
    serializer = PatientSerializer(patients, many=True)
    return Response({'patients': serializer.data})


# Vues HTML pour les patients
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


@login_required
def view_patient(request, patient_id):
    """Vue pour afficher les détails d'un patient avec un beau design"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Récupérer les documents et rapports associés
    from documents.models import Document
    from reports.models import Report
    
    documents = Document.objects.filter(patient=patient).order_by('-created_at')[:10]
    reports = Report.objects.filter(patient=patient).order_by('-created_at')[:10]
    
    # Calculer l'âge
    age = None
    if patient.date_of_birth:
        today = datetime.today()
        age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))
    
    context = {
        'patient': patient,
        'documents': documents,
        'reports': reports,
        'age': age,
    }
    
    return render(request, 'medical/patient_detail.html', context)


@login_required
def edit_patient(request, patient_id):
    """Vue pour éditer un patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # Mise à jour des champs
        patient.first_name = request.POST.get('first_name', patient.first_name)
        patient.last_name = request.POST.get('last_name', patient.last_name)
        patient.ci = request.POST.get('ci', patient.ci)
        patient.phone = request.POST.get('phone', patient.phone)
        patient.email = request.POST.get('email', patient.email)
        patient.address = request.POST.get('address', patient.address)
        patient.city = request.POST.get('city', patient.city)
        patient.blood_type = request.POST.get('blood_type', patient.blood_type)
        patient.emergency_contact = request.POST.get('emergency_contact', patient.emergency_contact)
        patient.insurance = request.POST.get('insurance', patient.insurance)
        patient.allergies = request.POST.get('allergies', patient.allergies)
        patient.medical_history = request.POST.get('medical_history', patient.medical_history)
        patient.occupation = request.POST.get('occupation', patient.occupation)
        patient.marital_status = request.POST.get('marital_status', patient.marital_status)
        patient.status = request.POST.get('status', patient.status)
        patient.notes = request.POST.get('notes', patient.notes)
        
        patient.save()
        messages.success(request, 'Patient modifié avec succès!')
        return redirect('view_patient', patient_id=patient.id)
    
    context = {
        'patient': patient,
    }
    
    return render(request, 'medical/patient_edit.html', context)


@login_required
def delete_patient(request, patient_id):
    """Vue pour supprimer un patient"""
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        patient_name = patient.get_full_name()
        patient.delete()
        messages.success(request, f'Le patient "{patient_name}" a été supprimé avec succès!')
    
    return redirect('patients')