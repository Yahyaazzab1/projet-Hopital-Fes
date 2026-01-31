"""
Utilitaires pour les notifications et l'historique
"""
from .models import Activity
from django.contrib.auth import get_user_model

User = get_user_model()


def log_activity(user, action, description, content_object=None, severity='info', details=None, request=None):
    """
    Enregistrer une activité dans l'historique
    
    Args:
        user: Utilisateur qui effectue l'action
        action: Type d'action (voir Activity.ACTION_CHOICES)
        description: Description de l'action
        content_object: Objet concerné (Patient, Document, etc.)
        severity: Niveau de sévérité (info, warning, error, critical)
        details: Détails supplémentaires (dict)
        request: Objet request Django (pour IP, user agent)
    
    Returns:
        Activity: L'objet Activity créé
    """
    activity_data = {
        'user': user,
        'action': action,
        'description': description,
        'severity': severity,
        'details': details or {}
    }
    
    # Ajouter l'objet concerné si fourni
    if content_object:
        activity_data['content_object'] = content_object
    
    # Ajouter les métadonnées de la requête si fournie
    if request:
        activity_data['ip_address'] = get_client_ip(request)
        activity_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:255]
        activity_data['session_key'] = request.session.session_key
    
    # Créer l'activité
    activity = Activity.objects.create(**activity_data)
    
    return activity


def get_client_ip(request):
    """
    Obtenir l'adresse IP du client
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Messages de notification prédéfinis
NOTIFICATION_MESSAGES = {
    # Patients
    'patient_created': {
        'title': 'Patient créé',
        'message': 'Le dossier patient a été créé avec succès',
        'type': 'success'
    },
    'patient_updated': {
        'title': 'Patient modifié',
        'message': 'Les informations du patient ont été mises à jour',
        'type': 'success'
    },
    'patient_deleted': {
        'title': 'Patient supprimé',
        'message': 'Le dossier patient a été archivé',
        'type': 'warning'
    },
    'patient_viewed': {
        'title': 'Dossier consulté',
        'message': 'Accès au dossier patient',
        'type': 'info'
    },
    
    # Documents
    'document_uploaded': {
        'title': 'Document téléchargé',
        'message': 'Le document a été ajouté avec succès',
        'type': 'success'
    },
    'document_processed': {
        'title': 'Document traité',
        'message': 'Le document a été analysé par l\'IA',
        'type': 'success'
    },
    'document_updated': {
        'title': 'Document modifié',
        'message': 'Le document a été mis à jour',
        'type': 'success'
    },
    'document_deleted': {
        'title': 'Document supprimé',
        'message': 'Le document a été archivé',
        'type': 'warning'
    },
    'document_downloaded': {
        'title': 'Document téléchargé',
        'message': 'Le document a été téléchargé',
        'type': 'info'
    },
    
    # Rapports
    'report_created': {
        'title': 'Rapport créé',
        'message': 'Le rapport médical a été créé',
        'type': 'success'
    },
    'report_updated': {
        'title': 'Rapport modifié',
        'message': 'Le rapport a été mis à jour',
        'type': 'success'
    },
    'report_deleted': {
        'title': 'Rapport supprimé',
        'message': 'Le rapport a été archivé',
        'type': 'warning'
    },
    'report_approved': {
        'title': 'Rapport approuvé',
        'message': 'Le rapport a été validé',
        'type': 'success'
    },
    'report_rejected': {
        'title': 'Rapport rejeté',
        'message': 'Le rapport a été rejeté',
        'type': 'error'
    },
    
    # Utilisateurs
    'user_created': {
        'title': 'Utilisateur créé',
        'message': 'Le compte utilisateur a été créé',
        'type': 'success'
    },
    'user_updated': {
        'title': 'Utilisateur modifié',
        'message': 'Le profil a été mis à jour',
        'type': 'success'
    },
    'user_deleted': {
        'title': 'Utilisateur supprimé',
        'message': 'Le compte a été désactivé',
        'type': 'warning'
    },
    
    # Système
    'login': {
        'title': 'Connexion réussie',
        'message': 'Bienvenue sur la plateforme',
        'type': 'success'
    },
    'logout': {
        'title': 'Déconnexion',
        'message': 'À bientôt !',
        'type': 'info'
    },
    'error_occurred': {
        'title': 'Erreur',
        'message': 'Une erreur s\'est produite',
        'type': 'error'
    },
    'security_alert': {
        'title': 'Alerte de sécurité',
        'message': 'Activité suspecte détectée',
        'type': 'urgent'
    },
}


def get_notification_message(action_key, custom_message=None):
    """
    Obtenir le message de notification pour une action
    
    Args:
        action_key: Clé de l'action
        custom_message: Message personnalisé (optionnel)
    
    Returns:
        dict: {title, message, type}
    """
    notification = NOTIFICATION_MESSAGES.get(action_key, {
        'title': 'Action effectuée',
        'message': custom_message or 'L\'action a été exécutée',
        'type': 'info'
    })
    
    if custom_message:
        notification['message'] = custom_message
    
    return notification


