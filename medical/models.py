from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import uuid

User = get_user_model()

class SoftDeleteManager(models.Manager):
    """Manager pour gérer les objets supprimés doucement"""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)

class SoftDeleteMixin(models.Model):
    """Mixin pour la suppression douce"""
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Supprimé par", related_name='soft_deleted_objects')
    deletion_reason = models.TextField(blank=True, verbose_name="Raison de la suppression")
    
    # Manager par défaut
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    class Meta:
        abstract = True
    
    def soft_delete(self, user=None, reason=""):
        """Suppression douce"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.deletion_reason = reason
        self.save()
    
    def restore(self):
        """Restaurer l'objet"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.deletion_reason = ""
        self.save()

class Activity(SoftDeleteMixin, models.Model):
    """Modèle pour enregistrer les activités des utilisateurs"""

    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('error', 'Erreur'),
        ('critical', 'Critique'),
    ]

    ACTION_CHOICES = [
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('patient_created', 'Patient créé'),
        ('patient_updated', 'Patient modifié'),
        ('patient_deleted', 'Patient supprimé'),
        ('patient_viewed', 'Patient consulté'),
        ('document_uploaded', 'Document téléchargé'),
        ('document_updated', 'Document modifié'),
        ('document_deleted', 'Document supprimé'),
        ('document_processed', 'Document traité'),
        ('document_downloaded', 'Document téléchargé'),
        ('report_created', 'Rapport créé'),
        ('report_updated', 'Rapport modifié'),
        ('report_deleted', 'Rapport supprimé'),
        ('report_approved', 'Rapport approuvé'),
        ('report_rejected', 'Rapport rejeté'),
        ('user_created', 'Utilisateur créé'),
        ('user_updated', 'Utilisateur modifié'),
        ('user_deleted', 'Utilisateur supprimé'),
        ('error_occurred', 'Erreur survenue'),
        ('security_alert', 'Alerte de sécurité'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name='activities')

    # Action et description
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Action")
    description = models.TextField(verbose_name="Description")

    # Niveau de sévérité
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info', verbose_name="Sévérité")

    # Objet concerné (relation générique)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Détails supplémentaires
    details = models.JSONField(default=dict, blank=True, verbose_name="Détails")

    # Métadonnées de la requête
    ip_address = models.CharField(max_length=45, blank=True, verbose_name="Adresse IP")
    user_agent = models.CharField(max_length=255, blank=True, verbose_name="Agent utilisateur")
    session_key = models.CharField(max_length=40, blank=True, verbose_name="Clé de session")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_display()} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    def get_severity_display(self):
        return dict(self.SEVERITY_CHOICES)[self.severity]

    def get_action_display(self):
        return dict(self.ACTION_CHOICES)[self.action]

class DeletedItem(models.Model):
    """Modèle pour stocker les informations sur les éléments supprimés"""
    DELETION_TYPES = [
        ('patient', 'Patient'),
        ('document', 'Document'),
        ('report', 'Rapport'),
        ('user', 'Utilisateur'),
        ('activity', 'Activité'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deletion_type = models.CharField(max_length=20, choices=DELETION_TYPES, verbose_name="Type d'élément")
    original_id = models.PositiveIntegerField(verbose_name="ID original")
    original_data = models.JSONField(verbose_name="Données originales")
    deletion_code = models.CharField(max_length=20, unique=True, verbose_name="Code de récupération")
    deleted_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de suppression")
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Supprimé par", related_name='deleted_items')
    deletion_reason = models.TextField(blank=True, verbose_name="Raison de la suppression")
    can_restore = models.BooleanField(default=True, verbose_name="Peut être restauré")
    
    class Meta:
        verbose_name = "Élément supprimé"
        verbose_name_plural = "Éléments supprimés"
        ordering = ['-deleted_at']
    
    def __str__(self):
        return f"{self.get_deletion_type_display()} #{self.original_id} - {self.deletion_code}"
    
    @classmethod
    def create_deletion_record(cls, obj, user, reason=""):
        """Créer un enregistrement de suppression"""
        import random
        import string
        
        # Générer un code unique
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while cls.objects.filter(deletion_code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Déterminer le type d'objet
        deletion_type = 'patient' if hasattr(obj, 'patient_id') else \
                       'document' if hasattr(obj, 'file') else \
                       'report' if hasattr(obj, 'report_type') else \
                       'user' if hasattr(obj, 'username') else \
                       'activity' if hasattr(obj, 'action') else 'unknown'
        
        # Sérialiser les données
        import json
        from datetime import date, datetime
        
        original_data = {}
        for field in obj._meta.fields:
            if field.name not in ['id', 'created_at', 'updated_at']:
                value = getattr(obj, field.name)
                if hasattr(value, 'pk'):  # ForeignKey
                    original_data[field.name] = value.pk
                elif hasattr(value, 'all'):  # ManyToManyField
                    original_data[field.name] = list(value.values_list('pk', flat=True))
                elif isinstance(value, (date, datetime)):
                    original_data[field.name] = value.isoformat()
                else:
                    original_data[field.name] = value
        
        return cls.objects.create(
            deletion_type=deletion_type,
            original_id=obj.pk,
            original_data=original_data,
            deletion_code=code,
            deleted_by=user,
            deletion_reason=reason
        )