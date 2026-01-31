```mermaid
classDiagram
    direction TB

    %% ============================================
    %% CLASSES PRINCIPALES - PLATEFORME MÉDICALE
    %% ============================================

    class User {
        +CharField username
        +CharField first_name
        +CharField last_name
        +EmailField email
        +CharField role (admin/doctor)
        +CharField department
        +CharField phone
        +BooleanField is_active
        +JSONField permissions
        +DateTimeField created_at
        +DateTimeField updated_at
        +get_full_name()
        +has_permission(permission)
        +get_role_display()
    }

    class Patient {
        +CharField patient_id (unique)
        +CharField first_name
        +CharField last_name
        +CharField carte_identite (unique)
        +DateField date_naissance
        +CharField genre (M/F/O)
        +CharField telephone
        +EmailField email
        +TextField adresse
        +CharField ville
        +CharField groupe_sanguin
        +CharField contact_urgence
        +CharField assurance
        +TextField allergies
        +TextField antecedents_medicaux
        +CharField profession
        +CharField etat_civil
        +CharField statut
        +TextField notes_medicales
        +ForeignKey created_by (User)
        +DateTimeField created_at
        +DateTimeField updated_at
        +get_full_name()
        +get_age()
        +get_documents_count()
        +get_reports_count()
    }

    class Document {
        +CharField titre
        +CharField type_document
        +TextField description
        +FileField fichier
        +IntegerField taille_fichier
        +CharField type_fichier
        +ForeignKey patient (Patient, nullable)
        +CharField nom_patient
        +CharField statut
        +CharField priorite
        +BooleanField traite_par_ia
        +FloatField confiance_ia
        +TextField texte_extrait_ia
        +JSONField decouvertes_ia
        +IntegerField score_qualite
        +DurationField temps_traitement
        +ForeignKey created_by (User)
        +ForeignKey assigned_doctor (User, nullable)
        +DateTimeField created_at
        +DateTimeField updated_at
        +get_file_size_display()
        +get_quality_display()
        +is_urgent()
    }

    class Report {
        +CharField titre
        +CharField type_rapport
        +TextField resume
        +TextField details
        +ForeignKey patient (Patient, nullable)
        +CharField nom_patient
        +CharField statut
        +CharField priorite
        +BooleanField traite_par_ia
        +JSONField insights_ia
        +TextField recommandations_ia
        +FloatField confiance_ia
        +TextField diagnostic
        +TextField traitement
        +JSONField medicaments
        +JSONField signes_vitaux
        +JSONField resultats_labo
        +ForeignKey created_by (User)
        +ForeignKey assigned_doctor (User, nullable)
        +ForeignKey reviewed_by (User, nullable)
        +DateTimeField review_date
        +ForeignKey validated_by (User, nullable)
        +DateTimeField validation_date
        +TextField admin_comments
        +DateTimeField report_date
        +JSONField attachments
        +get_status_display()
        +get_priority_display()
        +is_urgent()
    }

    class Activity {
        +UUIDField id (primary key)
        +ForeignKey user (User)
        +CharField action
        +TextField description
        +CharField severity (info/warning/error/critical)
        +GenericForeignKey content_object
        +JSONField details
        +CharField ip_address
        +CharField user_agent
        +CharField session_key
        +DateTimeField timestamp
        +get_severity_display()
        +get_action_display()
    }

    class DeletedItem {
        +UUIDField id (primary key)
        +CharField content_type
        +IntegerField object_id
        +JSONField original_data
        +CharField recovery_code (unique)
        +DateTimeField deleted_at
        +ForeignKey deleted_by (User)
        +TextField deletion_reason
        +BooleanField can_be_restored
        +create_deletion_record(obj, user, reason)
    }

    %% ============================================
    %% RELATIONS ENTRE CLASSES
    %% ============================================

    %% Relations Utilisateurs
    User "1" --> "1" UserProfile : profile
    User "1" --> "*" Patient : created_patients
    User "1" --> "*" Document : created_documents
    User "1" --> "*" Document : assigned_documents
    User "1" --> "*" Report : created_reports
    User "1" --> "*" Report : assigned_reports
    User "1" --> "*" Report : reviewed_reports
    User "1" --> "*" Report : validated_reports
    User "1" --> "*" Activity : user_activities
    User "1" --> "*" DeletedItem : deleted_items

    %% Relations Patients
    Patient "1" --> "*" Document : medical_documents
    Patient "1" --> "*" Report : medical_reports
    Patient "1" --> "*" PatientDocument : attachments

    %% Relations Documents
    Document "1" --> "*" DocumentTagRelation : tag_relations
    DocumentTag "1" --> "*" DocumentTagRelation : document_relations

    %% Relations Rapports
    Report "1" --> "*" ReportComment : comments
    Report "1" --> "*" ReportAttachment : attachments

    %% ============================================
    %% CONFIGURATION VISUELLE
    %% ============================================

    %% Styles pour différencier les types de classes
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef patientClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef documentClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef reportClass fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef activityClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#000
    classDef systemClass fill:#f5f5f5,stroke:#424242,stroke-width:1px,color:#000

    %% Application des styles
    class User userClass
    class UserProfile systemClass
    class Patient patientClass
    class Document documentClass
    class DocumentTag systemClass
    class DocumentTagRelation systemClass
    class Report reportClass
    class ReportTemplate systemClass
    class ReportComment systemClass
    class ReportAttachment systemClass
    class Activity activityClass
    class DeletedItem systemClass
    class PatientDocument patientClass

    %% ============================================
    %% NOTES D'IMPLEMENTATION
    %% ============================================

    note right of User : Roles disponibles :\n- admin : Administration complete\n- doctor : Gestion medicale\n- technician : Maintenance (non utilise)

    note right of Document : Traitement IA integre :\n- OCR automatique\n- Extraction de texte\n- Classification intelligente\n- Analyse de qualite

    note right of Report : Workflow validation :\n1. Brouillon\n2. Revision medicale\n3. Validation admin\n4. Approbation finale\n5. Publication

    note right of Activity : Audit complet :\n- 20 types d'actions\n- Generic Foreign Key\n- Logs avec IP et User-Agent

    note right of Patient : Dossier medical :\n- Informations personnelles\n- Antecedents medicaux\n- Coordonnees d'urgence
#### **📊 Rapports Médicaux**
- **Report** : Rapports médicaux avec workflow de validation
- **ReportTemplate** : Modèles prédéfinis de rapports
- **ReportComment** : Système de commentaires et annotations
- **Workflow** : Brouillon → Révision → Validation → Approbation → Publication

#### **📈 Traçabilité & Audit**
- **Activity** : Log complet de toutes les actions système
- **DeletedItem** : Système de suppression douce avec récupération
- **Audit Trail** : Traçabilité complète des modifications médicales

### 🔗 **Relations Principales :**

```
Utilisateur (1) ─── (N) Document : documents créés
Utilisateur (1) ─── (N) Report : rapports créés
Utilisateur (1) ─── (N) Patient : patients créés
Utilisateur (1) ─── (N) Activity : historique actions

Patient (1) ─── (N) Document : documents médicaux
Patient (1) ─── (N) Report : rapports médicaux
Patient (1) ─── (N) PatientDocument : pièces jointes

Document (1) ─── (N) DocumentTagRelation : tags de classification
Report (1) ─── (N) ReportComment : commentaires médicaux
```

### 🎯 **Fonctionnalités Clés :**

#### **🔐 Sécurité & Permissions**
- Système de rôles granulaire (admin/doctor/technician)
- Permissions JSON personnalisables
- Audit trail complet
- Suppression douce avec récupération

#### **🤖 Intelligence Artificielle**
- Traitement automatique des documents
- Extraction de texte OCR
- Analyse de qualité
- Génération d'insights médicaux

#### **📋 Workflows Médicaux**
- Validation hiérarchique des rapports
- Traçabilité des modifications
- Gestion des urgences
- Notifications en temps réel

#### **📊 Gestion Documentaire**
- Classification automatique
- Recherche full-text
- Export PDF/CSV
- Versioning implicite

**🏥 Plateforme médicale complète avec IA intégrée et traçabilité totale !**

**Note : Le rôle 'technician' est défini dans le modèle mais non utilisé dans l'interface actuelle.**
