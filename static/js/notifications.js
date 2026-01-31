/**
 * Système de notifications toast moderne
 */

class NotificationSystem {
    constructor() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    init() {
        // Créer le conteneur de notifications
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    }

    /**
     * Afficher une notification
     * @param {string} title - Titre de la notification
     * @param {string} message - Message de la notification
     * @param {string} type - Type: success, error, warning, info, urgent
     * @param {number} duration - Durée en millisecondes (0 = permanent)
     */
    show(title, message, type = 'info', duration = 5000) {
        const id = Date.now() + Math.random();
        
        // Icônes selon le type
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle',
            urgent: 'fa-bell'
        };

        const icon = icons[type] || icons.info;

        // Créer la notification
        const toast = document.createElement('div');
        toast.className = `notification-toast ${type}`;
        toast.setAttribute('data-id', id);
        toast.innerHTML = `
            <div class="notification-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-title">${title}</div>
                <div class="notification-message">${message}</div>
            </div>
            <button class="notification-close" onclick="notifications.close(${id})">
                <i class="fas fa-times"></i>
            </button>
            ${duration > 0 ? '<div class="notification-progress"></div>' : ''}
        `;

        // Ajouter au conteneur
        this.container.appendChild(toast);
        this.notifications.push({ id, toast, type });

        // Jouer un son selon le type
        this.playSound(type);

        // Fermer automatiquement après la durée spécifiée
        if (duration > 0) {
            setTimeout(() => {
                this.close(id);
            }, duration);
        }

        return id;
    }

    /**
     * Fermer une notification
     */
    close(id) {
        const notification = this.notifications.find(n => n.id === id);
        if (notification) {
            notification.toast.classList.add('closing');
            setTimeout(() => {
                if (notification.toast.parentNode) {
                    notification.toast.parentNode.removeChild(notification.toast);
                }
                this.notifications = this.notifications.filter(n => n.id !== id);
            }, 300);
        }
    }

    /**
     * Fermer toutes les notifications
     */
    closeAll() {
        this.notifications.forEach(n => {
            this.close(n.id);
        });
    }

    /**
     * Raccourcis pour les types courants
     */
    success(title, message, duration = 5000) {
        return this.show(title, message, 'success', duration);
    }

    error(title, message, duration = 7000) {
        return this.show(title, message, 'error', duration);
    }

    warning(title, message, duration = 6000) {
        return this.show(title, message, 'warning', duration);
    }

    info(title, message, duration = 5000) {
        return this.show(title, message, 'info', duration);
    }

    urgent(title, message, duration = 0) {
        return this.show(title, message, 'urgent', duration);
    }

    /**
     * Jouer un son selon le type
     */
    playSound(type) {
        // Sons optionnels (peut être désactivé)
        if (window.notificationSoundsEnabled === false) return;

        const sounds = {
            success: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSh+zPLTgjMGGGm98OScTgwOUKzn77dmHQU2jdXyy3ksBS...',
            error: 'data:audio/wav;base64,...',
            warning: 'data:audio/wav;base64,...',
        };

        if (sounds[type]) {
            try {
                const audio = new Audio(sounds[type]);
                audio.volume = 0.3;
                audio.play().catch(() => {
                    // Ignorer si l'audio ne peut pas être joué
                });
            } catch (e) {
                // Ignorer les erreurs audio
            }
        }
    }
}

// Créer une instance globale
window.notifications = new NotificationSystem();

// Fonctions d'aide globales
function showNotification(title, message, type = 'info', duration = 5000) {
    return window.notifications.show(title, message, type, duration);
}

function showSuccess(title, message) {
    return window.notifications.success(title, message);
}

function showError(title, message) {
    return window.notifications.error(title, message);
}

function showWarning(title, message) {
    return window.notifications.warning(title, message);
}

function showInfo(title, message) {
    return window.notifications.info(title, message);
}


