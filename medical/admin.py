from django.contrib import admin
from django.utils.html import format_html
from .models import DeletedItem


@admin.register(DeletedItem)
class DeletedItemAdmin(admin.ModelAdmin):
    """
    Administration du coffre-fort des suppressions
    """
    list_display = [
        'deletion_code',
        'get_deletion_type_display_colored',
        'original_id',
        'deleted_by',
        'deleted_at',
        'get_can_restore_display',
        'deletion_reason_short'
    ]
    
    list_filter = [
        'deletion_type',
        'deleted_at',
        'can_restore',
        'deleted_by'
    ]
    
    search_fields = [
        'deletion_code',
        'deletion_reason',
        'deleted_by__username',
        'deleted_by__first_name',
        'deleted_by__last_name'
    ]
    
    ordering = ['-deleted_at']
    
    readonly_fields = [
        'id',
        'deletion_code',
        'deletion_type',
        'original_id',
        'original_data',
        'deleted_at',
        'deleted_by'
    ]
    
    fieldsets = (
        ('Informations de suppression', {
            'fields': (
                'deletion_code',
                'deletion_type',
                'original_id',
                'deleted_at',
                'deleted_by'
            )
        }),
        ('Données originales', {
            'fields': ('original_data',),
            'classes': ('collapse',),
            'description': 'Données complètes de l\'élément supprimé'
        }),
        ('Raison et restauration', {
            'fields': (
                'deletion_reason',
                'can_restore'
            )
        }),
    )
    
    def get_deletion_type_display_colored(self, obj):
        """Afficher le type avec une couleur"""
        colors = {
            'patient': 'primary',
            'document': 'info',
            'report': 'success',
            'user': 'warning',
            'activity': 'secondary',
        }
        color = colors.get(obj.deletion_type, 'secondary')
        return format_html(
            '<span class="badge bg-{}" style="padding: 5px 10px; border-radius: 5px;">{}</span>',
            color,
            obj.get_deletion_type_display()
        )
    get_deletion_type_display_colored.short_description = 'Type'
    
    def get_can_restore_display(self, obj):
        """Afficher l'état de restauration"""
        if obj.can_restore:
            return format_html(
                '<span class="badge bg-success" style="padding: 5px 10px;">✅ Restaurable</span>'
            )
        return format_html(
            '<span class="badge bg-danger" style="padding: 5px 10px;">❌ Non restaurable</span>'
        )
    get_can_restore_display.short_description = 'État'
    
    def deletion_reason_short(self, obj):
        """Afficher la raison de manière courte"""
        if obj.deletion_reason:
            return obj.deletion_reason[:50] + ('...' if len(obj.deletion_reason) > 50 else '')
        return '-'
    deletion_reason_short.short_description = 'Raison'
    
    def has_add_permission(self, request):
        """Empêcher l'ajout manuel"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permettre la suppression définitive uniquement aux superusers"""
        return request.user.is_superuser
    
    actions = ['mark_as_non_restorable', 'delete_permanently']
    
    def mark_as_non_restorable(self, request, queryset):
        """Marquer les éléments comme non restaurables"""
        updated = queryset.update(can_restore=False)
        self.message_user(request, f'{updated} élément(s) marqué(s) comme non restaurable(s).')
    mark_as_non_restorable.short_description = "🔒 Marquer comme non restaurable"
    
    def delete_permanently(self, request, queryset):
        """Supprimer définitivement (seulement pour superuser)"""
        if request.user.is_superuser:
            count = queryset.count()
            queryset.delete()
            self.message_user(request, f'{count} élément(s) supprimé(s) définitivement.')
        else:
            self.message_user(request, 'Vous n\'avez pas la permission de supprimer définitivement.', level='error')
    delete_permanently.short_description = "🗑️ Supprimer définitivement (Admin uniquement)"
