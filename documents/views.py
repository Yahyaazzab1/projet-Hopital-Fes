from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Document, DocumentTag, DocumentTagRelation
from .serializers import DocumentSerializer, DocumentCreateSerializer, DocumentTagSerializer

class DocumentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentCreateSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        queryset = Document.objects.all()
        
        # Filtrage par recherche
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search)
            )
        
        # Filtrage par type de document
        doc_type = self.request.query_params.get('type', None)
        if doc_type:
            queryset = queryset.filter(document_type=doc_type)
        
        # Filtrage par statut
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Retourner le document créé avec le serializer complet (incluant id)."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        document = Document.objects.get(pk=serializer.instance.pk)
        output = DocumentSerializer(document, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DocumentCreateSerializer
        return DocumentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_stats_view(request):
    """Vue pour les statistiques des documents"""
    total_documents = Document.objects.count()
    processed_documents = Document.objects.filter(ai_processed=True).count()
    pending_documents = Document.objects.filter(status='pending').count()
    
    return Response({
        'total': total_documents,
        'processed': processed_documents,
        'pending': pending_documents
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_search_view(request):
    """Vue de recherche avancée des documents"""
    query = request.query_params.get('q', '')
    
    if len(query) < 2:
        return Response({'documents': []})
    
    documents = Document.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(patient__first_name__icontains=query) |
        Q(patient__last_name__icontains=query)
    )[:10]  # Limiter à 10 résultats
    
    serializer = DocumentSerializer(documents, many=True)
    return Response({'documents': serializer.data})


# Vues HTML pour les documents
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import base64


@login_required
def view_document(request, document_id):
    """Vue pour afficher un document avec design"""
    document = get_object_or_404(Document, id=document_id)
    
    # Extraire l'image base64 si elle est dans la description
    image_base64 = None
    if document.description and 'data:image' in document.description:
        # Extraire la partie base64
        if '[Image scannée: data:image' in document.description:
            start = document.description.find('data:image')
            end = document.description.find(']', start)
            if end > start:
                image_base64 = document.description[start:end]
    
    context = {
        'document': document,
        'image_base64': image_base64,
    }
    
    return render(request, 'medical/document_detail.html', context)


@login_required
def edit_document(request, document_id):
    """Vue pour éditer un document"""
    document = get_object_or_404(Document, id=document_id)
    
    if request.method == 'POST':
        document.title = request.POST.get('title', document.title)
        document.document_type = request.POST.get('document_type', document.document_type)
        document.status = request.POST.get('status', document.status)
        document.priority = request.POST.get('priority', document.priority)
        
        # Extraire la description sans l'image base64
        description = request.POST.get('description', '')
        if description and 'data:image' not in description:
            # Conserver l'image si elle existe
            if document.description and 'data:image' in document.description:
                # Garder l'image et mettre à jour le texte
                start = document.description.find('[Image scannée:')
                if start >= 0:
                    image_part = document.description[start:]
                    document.description = description + '\n\n' + image_part
                else:
                    document.description = description
            else:
                document.description = description
        
        document.save()
        messages.success(request, 'Document modifié avec succès!')
        return redirect('view_document', document_id=document.id)
    
    context = {
        'document': document,
    }
    
    return render(request, 'medical/document_edit.html', context)


@login_required
def delete_document(request, document_id):
    """Vue pour supprimer un document"""
    if request.method == 'POST':
        document = get_object_or_404(Document, id=document_id)
        document_title = document.title
        document.delete()
        messages.success(request, f'Le document "{document_title}" a été supprimé avec succès!')
    
    return redirect('documents')


@login_required
def download_document(request, document_id):
    """Vue pour télécharger l'image d'un document scanné"""
    document = get_object_or_404(Document, id=document_id)
    
    # Extraire l'image base64
    if document.description and 'data:image' in document.description:
        try:
            # Trouver la partie base64
            start = document.description.find('data:image')
            end = document.description.find(']', start)
            if end > start:
                data_url = document.description[start:end]
                
                # Extraire le type et les données
                header, encoded = data_url.split(',', 1)
                file_ext = header.split(';')[0].split('/')[-1]
                
                # Décoder le base64
                image_data = base64.b64decode(encoded)
                
                # Créer la réponse HTTP
                response = HttpResponse(image_data, content_type=f'image/{file_ext}')
                response['Content-Disposition'] = f'attachment; filename="{document.title}.{file_ext}"'
                return response
        except Exception as e:
            messages.error(request, f'Erreur lors du téléchargement: {str(e)}')
            return redirect('view_document', document_id=document.id)
    
    messages.error(request, 'Aucune image à télécharger')
    return redirect('view_document', document_id=document.id)