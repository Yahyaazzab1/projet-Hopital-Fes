# Diagramme de Cas d'Utilisation - Admin (Version Simplifiée)

## Architecture simplifiée conforme au code

```mermaid
graph TB
    Admin([👤 Admin])
    
    %% Cas d'utilisation principaux
    Auth[🔐 Connexion/Authentification]
    Users[👥 Gérer Utilisateurs<br/>Médecins, Infirmiers, Techniciens]
    Patients[🏥 Gérer Patients]
    Docs[📄 Gérer Documents]
    Reports[📊 Gérer Rapports]
    System[⚙️ Gérer Systèmes]
    Vault[🗄️ Coffre-fort Suppressions]
    
    %% Relations
    Admin --> Auth
    Admin --> Users
    Admin --> Patients
    Admin --> Docs
    Admin --> Reports
    Admin --> System
    Admin --> Vault
    
    style Admin fill:#dc3545,stroke:#333,stroke-width:3px,color:#fff
    style Auth fill:#007bff,stroke:#333,stroke-width:2px,color:#fff
    style Users fill:#28a745,stroke:#333,stroke-width:2px,color:#fff
    style Patients fill:#17a2b8,stroke:#333,stroke-width:2px,color:#fff
    style Docs fill:#ffc107,stroke:#333,stroke-width:2px,color:#212529
    style Reports fill:#6f42c1,stroke:#333,stroke-width:2px,color:#fff
    style System fill:#6c757d,stroke:#333,stroke-width:2px,color:#fff
    style Vault fill:#fd7e14,stroke:#333,stroke-width:2px,color:#fff
```

## Détails des fonctionnalités par module

### 👥 Gestion des Utilisateurs
**Route** : `/users/`

L'admin peut gérer **TOUS** les types d'utilisateurs dans une seule interface :
- ✅ Créer utilisateur (médecin, infirmier, technicien, admin)
- ✅ Modifier utilisateur
- ✅ Visualiser profil utilisateur
- ✅ Supprimer utilisateur
- ✅ Activer/Désactiver compte
- ✅ Modifier rôle

**✨ Changement important** : Plus de gestion séparée pour médecins et infirmiers !

### 🏥 Gestion des Patients
**Route** : `/patients/`
- Créer patient
- Modifier patient
- Visualiser dossier patient
- Supprimer patient

### 📄 Gestion des Documents
**Route** : `/documents/`
- Créer document
- Numériser document (Scanner)
- Traiter avec IA
- Modifier document
- Visualiser document
- Supprimer document

### 📊 Gestion des Rapports
**Route** : `/reports/`
- Créer rapport
- Modifier rapport
- Visualiser rapport
- Supprimer rapport
- Valider/Rejeter rapport

### ⚙️ Gestion des Systèmes
**Routes** : `/settings/`, `/system/*`
- Configurer système
- Consulter logs (`/system/logs/`)
- Gérer sauvegardes (`/system/backup/`)
- Monitoring (`/system/monitor/`)
- Maintenance (`/maintenance/`)

### 🗄️ Coffre-fort des Suppressions
**Route** : `/administration/deleted-items/`
- Consulter éléments supprimés
- Restaurer élément
- Supprimer définitivement

## Tableau de correspondance Code ↔ Diagramme

| Fonctionnalité Diagramme | URL dans le Code | Vue/Fonction |
|--------------------------|------------------|--------------|
| Gestion Utilisateurs | `/users/` | `users()` |
| Créer Utilisateur | POST `/users/` | `users()` POST |
| Voir Utilisateur | `/users/<id>/` | `view_user()` |
| Modifier Utilisateur | `/users/<id>/edit/` | `edit_user()` |
| Supprimer Utilisateur | `/users/<id>/delete/` | `delete_user()` |
| Gestion Patients | `/patients/` | `patients()` |
| Gestion Documents | `/documents/` | `documents()` |
| Scanner Documents | `/scanner/` | `scanner()` |
| Gestion Rapports | `/reports/` | `reports()` |
| Paramètres Système | `/settings/` | `settings_view()` |
| Logs Système | `/system/logs/` | `system_logs_view()` |
| Monitoring | `/system/monitor/` | `system_monitor_view()` |
| Sauvegardes | `/system/backup/` | `backup_restore_view()` |
| Maintenance | `/maintenance/` | `maintenance_view()` |
| Coffre-fort | `/administration/deleted-items/` | `deleted_items()` |
| Restaurer Item | `/administration/restore/<code>/` | `restore_item()` |

## Note importante

**🔴 Anciennes routes supprimées** :
- ~~`/doctors/`~~ → Maintenant dans `/users/`
- ~~`/nurses/`~~ → Jamais existé, toujours dans `/users/`
- ~~`/doctors/<id>/`~~ → Maintenant `/users/<id>/`
- ~~`/doctors/<id>/edit/`~~ → Maintenant `/users/<id>/edit/`

**✅ Le code est maintenant unifié et cohérent !**
