classDiagram
    direction TB

    %% ============================================
    %% CLASSES PRINCIPALES
    %% ============================================

    class Utilisateur {
        +CharField nom_utilisateur
        +CharField prenom
        +CharField nom
        +EmailField email
        +CharField role
        +CharField departement
        +CharField telephone
        +BooleanField est_actif
        +JSONField permissions
        +DateTimeField date_creation
        +DateTimeField date_modification
        +get_full_name()
        +has_permission()
        +get_role_display()
    }

    class ProfilUtilisateur {
        +ForeignKey utilisateur
        +ImageField avatar
        +CharField specialisation
        +CharField langue_preferee
        +JSONField preferences
        +DateField date_naissance
        +TextField adresse
        +CharField ville
        +CharField pays
        +CharField code_postal
        +CharField numero_licence
        +DateField date_embauche
        +get_full_address()
        +get_years_of_service()
    }

    class Patient {
        +CharField id_patient
        +CharField prenom
        +CharField nom
        +CharField carte_identite
        +DateField date_naissance
        +CharField genre
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
        +ForeignKey cree_par
        +DateTimeField date_creation
        +DateTimeField date_modification
        +DateTimeField derniere_visite
        +get_full_name()
        +get_age()
        +get_documents_count()
        +get_reports_count()
        +get_initials()
    }

    class Document {
        +CharField titre
        +CharField type_document
        +TextField description
        +FileField fichier
        +IntegerField taille_fichier
        +CharField type_fichier
        +ForeignKey patient
        +CharField nom_patient
        +CharField statut
        +CharField priorite
        +BooleanField traite_par_ia
        +FloatField confiance_ia
        +TextField texte_extrait_ia
        +JSONField decouvertes_ia
        +IntegerField score_qualite
        +CharField temps_traitement
        +ForeignKey cree_par
        +ForeignKey medecin
        +DateTimeField date_creation
        +DateTimeField date_modification
        +DateTimeField date_traitement
        +DateField date_document
        +get_file_size_display()
        +get_quality_display()
        +is_urgent()
        +get_processing_status_display()
    }

    class Rapport {
        +CharField titre
        +CharField type_rapport
        +TextField resume
        +TextField details
        +ForeignKey patient
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
        +ForeignKey cree_par
        +ForeignKey medecin
        +ForeignKey revise_par
        +DateTimeField date_revision
        +ForeignKey valide_par
        +DateTimeField date_validation
        +TextField commentaires_admin
        +DateTimeField date_rapport
        +JSONField pieces_jointes
        +get_status_display_color()
        +get_priority_display_color()
        +is_urgent()
        +get_ai_confidence_display()
        +get_attachments_count()
    }

    class Activite {
        +UUIDField id
        +ForeignKey utilisateur
        +CharField action
        +TextField description
        +CharField severite
        +CharField objet_concerne
        +JSONField details
        +GenericIPAddressField adresse_ip
        +CharField agent_utilisateur
        +CharField cle_session
        +DateTimeField date_creation
        +get_severity_display()
        +get_action_display()
    }

    class ElementSupprime {
        +UUIDField id
        +CharField type_element
        +IntegerField id_original
        +JSONField donnees_originales
        +CharField code_recuperation
        +DateTimeField date_suppression
        +ForeignKey supprime_par
        +TextField raison_suppression
        +BooleanField peut_etre_restore
        +create_deletion_record()
    }

    class TagDocument {
        +CharField nom
        +CharField couleur
        +TextField description
        +CharField categorie
        +IntegerField ordre
        +BooleanField est_actif
        +get_usage_count()
        +get_color_display()
    }

    class RelationTagDocument {
        +ForeignKey document
        +ForeignKey tag
        +DateTimeField date_creation
    }

    class CommentaireRapport {
        +ForeignKey rapport
        +ForeignKey auteur
        +TextField contenu
        +CharField type_commentaire
        +BooleanField est_resolu
        +IntegerField ligne_reference
        +CharField section_reference
        +DateTimeField date_creation
        +DateTimeField date_modification
        +get_short_content()
        +is_urgent()
    }

    class ModeleRapport {
        +CharField nom
        +TextField description
        +TextField template
        +CharField type_rapport
        +BooleanField est_actif
        +ForeignKey cree_par
        +DateTimeField date_creation
    }

    class DocumentPatient {
        +CharField titre
        +TextField description
        +FileField fichier
        +ForeignKey patient
        +ForeignKey cree_par
        +DateTimeField date_creation
    }

    %% ============================================
    %% RELATIONS ENTRE CLASSES
    %% ============================================

    %% Relations Utilisateurs (1 vers 1 et 1 vers N)
    Utilisateur "1" --> "1" ProfilUtilisateur : profile
    Utilisateur "1" --> "*" Patient : patients_crees
    Utilisateur "1" --> "*" Document : documents_crees
    Utilisateur "1" --> "*" Document : documents_medecin
    Utilisateur "1" --> "*" Rapport : rapports_crees
    Utilisateur "1" --> "*" Rapport : rapports_medecin
    Utilisateur "1" --> "*" Rapport : rapports_revises
    Utilisateur "1" --> "*" Rapport : rapports_valides
    Utilisateur "1" --> "*" Activite : activites
    Utilisateur "1" --> "*" ElementSupprime : elements_supprimes

    %% Relations Patients (1 vers N)
    Patient "1" --> "*" Document : documents_medicaux
    Patient "1" --> "*" Rapport : rapports
    Patient "1" --> "*" DocumentPatient : documents

    %% Relations Documents (1 vers N et N vers N)
    Document "1" --> "*" RelationTagDocument : relations_tags
    TagDocument "1" --> "*" RelationTagDocument : relations_documents

    %% Relations Rapports (1 vers N)
    Rapport "1" --> "*" CommentaireRapport : commentaires

    %% ============================================
    %% CONFIGURATION VISUELLE
    %% ============================================

    %% Styles pour differencier les types de classes
    classDef classeUtilisateur fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef classePatient fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef classeDocument fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef classeRapport fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef classeActivite fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#000
    classDef classeSysteme fill:#f5f5f5,stroke:#424242,stroke-width:1px,color:#000

    %% Application des styles
    class Utilisateur classeUtilisateur
    class ProfilUtilisateur classeUtilisateur
    class Patient classePatient
    class Document classeDocument
    class TagDocument classeSysteme
    class RelationTagDocument classeSysteme
    class Rapport classeRapport
    class ModeleRapport classeSysteme
    class CommentaireRapport classeSysteme
    class Activite classeActivite
    class ElementSupprime classeSysteme
    class DocumentPatient classePatient

    %% ============================================
    %% NOTES D'IMPLEMENTATION
    %% ============================================

    note right of Utilisateur : Roles disponibles :\n- admin : Administration complete\n- doctor : Gestion medicale\n- technician : Maintenance systeme (non utilise)

    note right of Document : IA integree :\n- OCR automatique\n- Extraction de texte\n- Classification intelligente\n- Analyse de qualite\n- Score de confiance

    note right of Rapport : Workflow de validation :\n1. Brouillon\n2. Revision medicale\n3. Validation admin\n4. Approbation finale\n5. Publication

    note right of Activite : Tracabilite complete :\n- 20 types d'actions\n- Audit trail complet\n- Generic Foreign Key\n- Logs avec IP et User-Agent

    note right of Patient : Dossier medical complet :\n- Informations personnelles\n- Antecedents medicaux\n- Coordonnees d'urgence\n- Historique des consultations

    note right of ElementSupprime : Suppression douce :\n- Sauvegarde automatique\n- Codes de recuperation\n- Restauration en 1 clic\n- Conformite medicale
```

## 📋 **Plateforme Médicale AL GHASSANI - Diagramme de Classe**

### 🏗️ **Vue d'ensemble de l'architecture**

Le diagramme présente une **plateforme médicale Django complète** avec **IA intégrée** et **traçabilité totale**. L'architecture modulaire organise autour de **six entités principales** : Utilisateur, Patient, Document, Rapport, Activite, et ElementSupprime, avec des **relations complexes** et des **fonctionnalités avancées** pour la gestion hospitalière.

---

## 👥 **Système de Gestion des Utilisateurs**

### **Modèle User central :**
- **Architecture multi-rôles** (admin/doctor) avec permissions granulaires
- **Extensions de profil** via ProfilUtilisateur avec détails professionnels
- **Fonctionnalités de sécurité** (tracking IP, gestion sessions)
- **Intégration audit** pour traçabilité complète des activités

### **Contrôle d'accès :**
```
Admin: Accès complet + gestion utilisateurs
Doctor: Gestion patients + traitement documents + création rapports
```

---

## 🏥 **Module de Gestion des Patients**

### **Dossiers médicaux complets :**
- **Identification personnelle** (patient_id unique, CI, données démographiques)
- **Informations médicales** (groupe sanguin, allergies, antécédents)
- **Gestion contacts** (urgence, assurance)
- **Suivi statuts** (actif/inactif/décédé/transféré)
- **Calculs dynamiques** (âge, décompte documents/rapports)

---

## 📄 **Gestion Documentaire Intelligente**

### **Traitement IA avancé :**
- **Extraction automatique de texte** depuis images/PDF médicaux
- **Score qualité** et métriques de confiance (0-100%)
- **Traitement prioritaire** (faible/normal/élevé/urgent)
- **Workflow statuts** (en_attente → traitement → terminé)
- **Assignation professionnelle** (créé_par/médecin)

### **Classification et Tagging :**
- **Système de tags dynamiques** via TagDocument et RelationTagDocument
- **Organisation visuelle** avec catégories codées par couleur
- **Recherche et filtrage** avancés

---

## 📊 **Système de Rapports Médicaux**

### **Workflow de validation 5 étapes :**
1. **Draft** → 2. **Pending Review** → 3. **Validated** → 4. **Approved** → 5. **Published**

### **Intégration IA :**
- **Génération automatique d'insights** depuis données patients
- **Recommandations de traitement** basées sur analyse médicale
- **Score de confiance** pour contenu généré par IA
- **Intégration** signes vitaux et résultats de laboratoire

### **Fonctionnalités collaboratives :**
- **Processus de révision multi-utilisateurs** (doctor/reviewed_by/validated_by)
- **Système de commentaires** via CommentaireRapport
- **Support templates** via ModeleRapport
- **Gestion pièces jointes** avec métadonnées JSON

---

## 📈 **Système d'Audit et Conformité**

### **Traçabilité complète :**
- **20 types d'actions** trackées (login, create, update, delete, etc.)
- **Relations clé étrangère génériques** pour association flexible d'objets
- **Logs IP et User-Agent** pour sécurité
- **Tracking sessions** et métadonnées détaillées

### **Implémentation Soft Delete :**
- **Préservation complète des données** avec sérialisation JSON
- **Codes de récupération** (identifiants uniques alphanumériques 8 caractères)
- **Capacités de restauration** pour récupération de données
- **Tracking raison de suppression** et responsabilité utilisateur

---

## 🔗 **Architecture des Relations**

### **Design de Cardinalité :**
```
User (1) ─── (N) Patient : relation de création
User (1) ─── (N) Document : création et responsabilité médicale
User (1) ─── (N) Report : workflow de validation multi-étapes
User (1) ─── (N) Activity : audit trail complet

Patient (1) ─── (N) Document : association dossier médical
Patient (1) ─── (N) Report : historique traitements et diagnostics

Document (1) ─── (N) TagDocument : système de classification
Report (1) ─── (N) CommentaireRapport : annotations collaboratives
```

---

## 🎯 **Implémentation Technique**

### **Points forts :**
- **Intégration IA** : OCR, classification, génération d'insights
- **Fonctionnalités sécurité** : permissions granulaires, suppression douce
- **Trails d'audit complets** : conformité médicale
- **Optimisations performance** : index, contraintes, JSON flexible

### **Conformité médicale :**
- **Préservation données** selon lois dossiers médicaux
- **Audit complet** pour inspections réglementaires
- **Responsabilité utilisateur** avec tracking actions complet
- **Workflows validation** pour rapports médicaux

---

**Plateforme médicale d'entreprise avec IA intégrée, audit complet et conformité légale - Architecture robuste pour hôpital moderne.**

## 📋 **Diagramme de Classe - Plateforme Médicale AL GHASSANI**

### 🏗️ **Architecture Modulaire Django**

#### **1. Système d'Utilisateurs**
- **Utilisateur** : Authentification et gestion des rôles
- **ProfilUtilisateur** : Extensions avec avatar, spécialisations, langues

#### **2. Gestion des Patients**
- **Patient** : Dossier médical complet avec métadonnées
- **DocumentPatient** : Documents spécifiques aux patients (legacy)

#### **3. Documents Médicaux IA**
- **Document** : Traitement intelligent avec OCR et classification
- **TagDocument** : Système de classification et d'indexation
- **RelationTagDocument** : Association documents-tags

#### **4. Rapports Médicaux**
- **Rapport** : Workflow de validation avec IA intégrée
- **ModeleRapport** : Templates prédéfinis de rapports
- **CommentaireRapport** : Système de commentaires médicaux

#### **5. Traçabilité et Audit**
- **Activite** : Log complet de toutes les actions système
- **ElementSupprime** : Système de suppression douce avec récupération

---

## 🔗 **Relations Principales**

### **Cardinalité et Navigation :**
```
Utilisateur (1) ─── (1) ProfilUtilisateur : profile étendu
Utilisateur (1) ─── (N) Patient : patients créés
Utilisateur (1) ─── (N) Document : documents créés/traités
Utilisateur (1) ─── (N) Rapport : rapports créés/révisés/validés
Utilisateur (1) ─── (N) Activite : historique des actions

Patient (1) ─── (N) Document : documents médicaux
Patient (1) ─── (N) Rapport : rapports médicaux
Patient (1) ─── (N) DocumentPatient : pièces jointes

Document (1) ─── (N) RelationTagDocument : tags de classification
Rapport (1) ─── (N) CommentaireRapport : annotations médicales
```

---

## 🎯 **Méthodes et Fonctionnalités**

### **Utilisateur :**
- `get_full_name()` : Nom complet formaté
- `get_short_name()` : Prénom seulement
- `get_initials()` : Initiales du nom
- `has_permission()` : Vérification des droits
- `get_role_display()` : Nom du rôle en français

### **Patient :**
- `get_full_name()` : Nom complet du patient
- `get_age()` : Calcul de l'âge actuel
- `get_documents_count()` : Nombre de documents
- `get_reports_count()` : Nombre de rapports
- `get_initials()` : Initiales du patient

### **Document :**
- `get_file_size_display()` : Taille formatée
- `get_quality_display()` : Qualité du document
- `is_urgent()` : Vérification d'urgence
- `get_processing_status_display()` : Statut traitement

### **Rapport :**
- `get_status_display_color()` : Couleur du statut
- `get_priority_display_color()` : Couleur priorité
- `is_urgent()` : Vérification d'urgence
- `get_ai_confidence_display()` : Niveau de confiance IA
- `get_attachments_count()` : Nombre de pièces jointes

### **Activite :**
- `get_severity_display()` : Niveau de sévérité
- `get_action_display()` : Description de l'action

### **ElementSupprime :**
- `create_deletion_record()` : Création sauvegarde suppression

---

## 🔐 **Contraintes et Index**

### **Index optimisés :**
- **Patient** : id_patient, carte_identite, nom+prénom, statut
- **Document** : type_document, statut, priorité, traite_par_ia
- **Rapport** : type_rapport, statut, priorité, traite_par_ia
- **Activite** : date_creation, utilisateur, action

### **Contraintes d'intégrité :**
- **unicité** : id_patient, carte_identite, email, nom_utilisateur
- **référentielle** : ForeignKey avec CASCADE/SET_NULL
- **domaine** : Choix limités (GENDER, TYPE, STATUS, etc.)

---

## 🏥 **Conformité Médicale**

### **Rôles et Permissions :**
- **Admin** : Accès complet + administration
- **Médecin** : CRUD patients + documents + rapports
- **Infirmier** : Consultation + modification (pas création)
- **Technicien** : Monitoring + maintenance (pas médical)

### **Traçabilité :**
- **Audit trail** complet pour inspections médicales
- **Suppression douce** avec récupération possible
- **Logs détaillés** avec IP, timestamp, utilisateur
- **Conservation** des données selon réglementation

---

**Diagramme de classe complet en français avec tous les attributs, relations et méthodes !**

**Architecture modulaire, traçabilité complète et conformité médicale respectée.**
