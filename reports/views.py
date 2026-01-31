from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
import unicodedata
import re
from django.conf import settings
import os
from .models import Report, ReportComment, ReportTemplate
from .serializers import ReportSerializer, ReportCreateSerializer, ReportCommentSerializer
from .forms import ReportForm
from patients.models import Patient
from users.models import User

class ReportListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReportCreateSerializer
        return ReportSerializer
    
    def get_queryset(self):
        queryset = Report.objects.all()
        
        # Filtrage par recherche
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(summary__icontains=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search)
            )
        
        # Filtrage par type de rapport
        report_type = self.request.query_params.get('type', None)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        
        # Filtrage par statut
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-report_date')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReportCreateSerializer
        return ReportSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_stats_view(request):
    """Vue pour les statistiques des rapports"""
    total_reports = Report.objects.count()
    completed_reports = Report.objects.filter(status='completed').count()
    pending_reports = Report.objects.filter(status='pending').count()
    
    return Response({
        'total': total_reports,
        'completed': completed_reports,
        'pending': pending_reports
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_search_view(request):
    """Vue de recherche avancée des rapports"""
    query = request.query_params.get('q', '')
    
    if len(query) < 2:
        return Response({'reports': []})
    
    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(patient__first_name__icontains=query) |
        Q(patient__last_name__icontains=query)
    )[:10]  # Limiter à 10 résultats
    
    serializer = ReportSerializer(reports, many=True)
    return Response({'reports': serializer.data})

# Vues frontend pour les rapports
@login_required
def report_add_view(request):
    """Vue pour ajouter un nouveau rapport"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            messages.success(request, 'Rapport créé avec succès!')
            return redirect('reports')
    else:
        form = ReportForm()
    
    # Récupérer les patients actifs pour le formulaire
    patients = Patient.objects.filter(status='active')
    
    context = {
        'form': form,
        'patients': patients,
        'report_types': Report.TYPE_CHOICES,
        'status_choices': Report.STATUS_CHOICES,
        'priority_choices': Report.PRIORITY_CHOICES,
    }
    
    return render(request, 'reports/report_add.html', context)


@login_required
def view_report(request, report_id):
    """Vue pour afficher un rapport"""
    from django.shortcuts import get_object_or_404
    
    report = get_object_or_404(Report, id=report_id)
    
    context = {
        'report': report,
    }
    
    return render(request, 'medical/report_detail.html', context)


@login_required
def edit_report(request, report_id):
    """Vue pour éditer un rapport"""
    from django.shortcuts import get_object_or_404
    
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            updated_report = form.save(commit=False)
            updated_report.updated_by = request.user
            updated_report.save()
            messages.success(request, 'Rapport modifié avec succès!')
            return redirect('reports')
    else:
        form = ReportForm(instance=report)
    
    patients = Patient.objects.filter(status='active')
    doctors = User.objects.filter(role='doctor', is_active=True)
    
    context = {
        'form': form,
        'report': report,
        'patients': patients,
        'doctors': doctors,
        'report_types': Report.TYPE_CHOICES,
        'status_choices': Report.STATUS_CHOICES,
        'priority_choices': Report.PRIORITY_CHOICES,
    }
    
    return render(request, 'medical/report_edit.html', context)


@login_required
def delete_report(request, report_id):
    """Vue pour supprimer un rapport"""
    from django.shortcuts import get_object_or_404
    
    if request.method == 'POST':
        report = get_object_or_404(Report, id=report_id)
        report_title = report.title
        report.delete()
        messages.success(request, f'Le rapport "{report_title}" a été supprimé avec succès!')
    
    return redirect('reports')


# ===== VALIDATION ADMINISTRATIVE =====

@login_required
def admin_validation_view(request):
    """
    Vue pour la validation administrative des rapports
    Accessible uniquement aux administrateurs
    """
    # Vérifier que l'utilisateur est admin
    if not request.user.is_staff:
        messages.error(request, 'Accès refusé. Cette fonctionnalité est réservée aux administrateurs.')
        return redirect('dashboard')
    
    # Récupérer les rapports en attente de validation
    pending_reports = Report.objects.filter(
        status='pending_validation'
    ).select_related('patient', 'created_by').order_by('-report_date')
    
    # Récupérer les rapports récemment validés
    validated_reports = Report.objects.filter(
        status__in=['validated', 'rejected']
    ).select_related('patient', 'created_by').order_by('-validation_date')[:10]
    
    context = {
        'pending_reports': pending_reports,
        'validated_reports': validated_reports,
        'total_pending': pending_reports.count(),
    }
    
    return render(request, 'reports/admin_validation.html', context)


@login_required
def validate_report_view(request, report_id):
    """
    Vue pour valider ou rejeter un rapport spécifique
    """
    # Vérifier que l'utilisateur est admin
    if not request.user.is_staff:
        messages.error(request, 'Accès refusé.')
        return redirect('dashboard')
    
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_comment = request.POST.get('admin_comment', '')
        
        if action == 'validate':
            report.status = 'validated'
            report.validation_date = timezone.now()
            report.validated_by = request.user
            report.admin_comment = admin_comment
            report.save()
            
            messages.success(request, f'Le rapport "{report.title}" a été validé avec succès.')
            
        elif action == 'reject':
            report.status = 'rejected'
            report.validation_date = timezone.now()
            report.validated_by = request.user
            report.admin_comment = admin_comment
            report.save()
            
            messages.warning(request, f'Le rapport "{report.title}" a été rejeté.')
            
        elif action == 'return':
            report.status = 'draft'
            report.validation_date = timezone.now()
            report.validated_by = request.user
            report.admin_comment = admin_comment
            report.save()
            
            messages.info(request, f'Le rapport "{report.title}" a été retourné au médecin pour modifications.')
        
        return redirect('admin_validation')
    
    # Récupérer l'historique des validations
    validation_history = Report.objects.filter(
        patient=report.patient
    ).exclude(id=report_id).filter(
        validation_date__isnull=False
    ).order_by('-validation_date')[:5]
    
    context = {
        'report': report,
        'validation_history': validation_history,
    }
    
    return render(request, 'reports/validate_report_detail.html', context)


# ===== EXPORT PDF =====

@login_required
def export_report_pdf(request, report_id):
    """
    Vue pour exporter un rapport en PDF avec mise en page professionnelle
    """
    report = get_object_or_404(Report, id=report_id)
    
    # Vérifier les permissions (médecin, admin, ou créateur du rapport)
    if not (request.user.is_staff or 
            request.user.role in ['doctor', 'admin'] or 
            report.created_by == request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('reports')
    
    # Générer le PDF
    try:
        # Créer le contenu HTML
        html_content = render_to_string('reports/report_pdf.html', {
            'report': report,
            'hospital_info': {
                'name': 'Hôpital AL GHASSANI',
                'address': '123 Avenue Mohammed V, Casablanca, Maroc',
                'phone': '+212 5 22 XX XX XX',
                'email': 'contact@elghassani.ma',
                'logo': '/static/img/logo.png',  # Logo de l'hôpital
            },
            'generated_at': timezone.now(),
            'generated_by': request.user.get_full_name(),
        })
        
        # Simuler la génération PDF (en production, utiliser weasyprint ou reportlab)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="rapport_{report.id}_{report.patient.get_full_name() if report.patient else "patient"}.pdf"'
        
        # Pour la démonstration, retourner un message de succès
        # En production, remplacer par la vraie génération PDF
        # Sanitize helper: strip accents and escape PDF special characters
        def sanitize(text):
            if text is None:
                return 'N/A'
            # remove accents
            no_accents = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')
            # escape parentheses and backslashes for PDF text objects
            no_accents = no_accents.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')
            return no_accents

        hospital_line = 'Rapport Medical - Hopital AL GHASSANI'
        patient_line = f"Patient: {sanitize(report.patient.get_full_name() if report.patient else 'N/A')}"
        title_line = f"Titre: {sanitize(report.title)}"
        date_line = f"Date: {report.report_date.strftime('%d/%m/%Y')}"
        type_display = report.get_report_type_display() if hasattr(report, 'get_report_type_display') else report.report_type
        type_line = f"Type: {sanitize(type_display)}"
        doctor_name = report.doctor.get_full_name() if hasattr(report, 'doctor') and report.doctor else 'N/A'
        doctor_line = f"Medecin: {sanitize(doctor_name)}"
        status_display = report.get_status_display() if hasattr(report, 'get_status_display') else report.status
        status_line = f"Statut: {sanitize(status_display)}"
        priority_display = report.get_priority_display() if hasattr(report, 'get_priority_display') else report.priority
        priority_line = f"Priorite: {sanitize(priority_display)}"
        summary_text = (report.summary[:80] + '...') if report.summary else 'N/A'
        summary_line = f"Resume: {sanitize(summary_text)}"

        response.write(f"""
        %PDF-1.4
        1 0 obj
        <<
        /Type /Catalog
        /Pages 2 0 R
        >>
        endobj
        
        2 0 obj
        <<
        /Type /Pages
        /Kids [3 0 R]
        /Count 1
        >>
        endobj
        
        3 0 obj
        <<
        /Type /Page
        /Parent 2 0 R
        /MediaBox [0 0 612 792]
        /Contents 4 0 R
        >>
        endobj
        
        4 0 obj
        <<
        /Length 700
        >>
        stream
        BT
        /F1 12 Tf
        72 720 Td
        ({sanitize(hospital_line)}) Tj
        0 -20 Td
        ({patient_line}) Tj
        0 -20 Td
        ({title_line}) Tj
        0 -20 Td
        ({date_line}) Tj
        0 -20 Td
        ({type_line}) Tj
        0 -20 Td
        ({doctor_line}) Tj
        0 -20 Td
        ({status_line}) Tj
        0 -20 Td
        ({priority_line}) Tj
        0 -20 Td
        ({summary_line}) Tj
        ET
        endstream
        endobj
        
        xref
        0 5
        0000000000 65535 f 
        0000000009 00000 n 
        0000000058 00000 n 
        0000000115 00000 n 
        0000000204 00000 n 
        trailer
        <<
        /Size 5
        /Root 1 0 R
        >>
        startxref
        454
        %%EOF
        """)
        
        return response
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la génération du PDF: {str(e)}')
        return redirect('view_report', report_id=report_id)


@login_required
def export_reports_list_pdf(request):
    """
    Vue pour exporter une liste de rapports en PDF
    """
    # Vérifier les permissions
    if not (request.user.is_staff or request.user.role in ['doctor', 'admin']):
        messages.error(request, 'Accès refusé.')
        return redirect('reports')
    
    # Récupérer les rapports selon les filtres
    reports = Report.objects.all().order_by('-report_date')[:50]  # Limiter à 50 rapports
    
    # Générer le PDF
    try:
        html_content = render_to_string('reports/reports_list_pdf.html', {
            'reports': reports,
            'hospital_info': {
                'name': 'Hôpital EL GHASSANI',
                'address': '123 Avenue Mohammed V, Casablanca, Maroc',
                'phone': '+212 5 22 XX XX XX',
                'email': 'contact@elghassani.ma',
                'logo': '/static/img/logo.png',
            },
            'generated_at': timezone.now(),
            'generated_by': request.user.get_full_name(),
            'total_reports': reports.count(),
        })
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="liste_rapports_medicaux.pdf"'
        
        # Simuler la génération PDF
        response.write(f"""
        %PDF-1.4
        1 0 obj
        <<
        /Type /Catalog
        /Pages 2 0 R
        >>
        endobj
        
        2 0 obj
        <<
        /Type /Pages
        /Kids [3 0 R]
        /Count 1
        >>
        endobj
        
        3 0 obj
        <<
        /Type /Page
        /Parent 2 0 R
        /MediaBox [0 0 612 792]
        /Contents 4 0 R
        >>
        endobj
        
        4 0 obj
        <<
        /Length 300
        >>
        stream
        BT
        /F1 14 Tf
        72 720 Td
        (Liste des Rapports Médicaux) Tj
        0 -25 Td
        /F1 12 Tf
        (Hôpital EL GHASSANI) Tj
        0 -20 Td
        (Généré le: {timezone.now().strftime('%d/%m/%Y à %H:%M')}) Tj
        0 -20 Td
        (Total: {reports.count()} rapports) Tj
        0 -30 Td
        ET
        endstream
        endobj
        
        xref
        0 5
        0000000000 65535 f 
        0000000009 00000 n 
        0000000058 00000 n 
        0000000115 00000 n 
        0000000204 00000 n 
        trailer
        <<
        /Size 5
        /Root 1 0 R
        >>
        startxref
        554
        %%EOF
        """)
        
        return response
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la génération du PDF: {str(e)}')
        return redirect('reports')