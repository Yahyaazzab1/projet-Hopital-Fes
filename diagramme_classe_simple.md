```mermaid
classDiagram
    %% ============================================
    %% CLASSES PRINCIPALES
    %% ============================================

    class Utilisateur {
        +String nom_utilisateur
        +String prenom
        +String nom
        +String email
        +String role
        +String departement
        +String telephone
        +Boolean est_actif
        +DateTime date_creation
        +get_full_name()
        +has_permission()
    }

    class Patient {
        +String id_patient
        +String prenom
        +String nom
        +String carte_identite
        +Date date_naissance
        +String genre
        +String telephone
        +String email
        +String adresse
        +String ville
        +String groupe_sanguin
        +String contact_urgence
        +String assurance
        +String allergies
        +String antecedents_medicaux
        +String profession
        +String etat_civil
        +String statut
        +String notes_medicales
        +DateTime date_creation
        +get_full_name()
        +get_age()
    }

    class Document {
        +String titre
        +String type_document
        +String description
        +File fichier
        +Integer taille_fichier
        +String patient
        +String nom_patient
        +String statut
        +String priorite
        +Boolean traite_par_ia
        +Float confiance_ia
        +String texte_extrait_ia
        +DateTime date_creation
        +get_quality_display()
        +is_urgent()
    }

    class Rapport {
        +String titre
        +String type_rapport
        +String resume
        +String details
        +String patient
        +String nom_patient
        +String statut
        +String priorite
        +Boolean traite_par_ia
        +Float confiance_ia
        +String diagnostic
        +String traitement
        +DateTime date_rapport
        +get_ai_confidence_display()
        +is_urgent()
    }

    class Activite {
        +UUID id
        +String utilisateur
        +String action
        +String description
        +String severite
        +DateTime date_creation
        +get_severity_display()
        +get_action_display()
    }

    class ElementSupprime {
        +UUID id
        +String type_element
        +Integer id_original
        +JSON donnees_originales
        +String code_recuperation
        +DateTime date_suppression
        +String raison_suppression
        +Boolean peut_etre_restore
    }

    %% ============================================
    %% RELATIONS
    %% ============================================

    Utilisateur "1" --> "1" ProfilUtilisateur : profile
    Utilisateur "1" --> "*" Patient : patients_crees
    Utilisateur "1" --> "*" Document : documents_crees
    Utilisateur "1" --> "*" Rapport : rapports_crees
    Utilisateur "1" --> "*" Activite : activites
    Utilisateur "1" --> "*" ElementSupprime : elements_supprimes

    Patient "1" --> "*" Document : documents_medicaux
    Patient "1" --> "*" Rapport : rapports

    Document "1" --> "*" TagDocument : tags
    Rapport "1" --> "*" CommentaireRapport : commentaires

    %% ============================================
    %% STYLES
    %% ============================================

    classDef utilisateurClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef patientClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef documentClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef rapportClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef activiteClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef systemeClass fill:#f5f5f5,stroke:#424242,stroke-width:1px

    class Utilisateur utilisateurClass
    class ProfilUtilisateur utilisateurClass
    class Patient patientClass
    class Document documentClass
    class TagDocument systemeClass
    class Rapport rapportClass
    class CommentaireRapport systemeClass
    class Activite activiteClass
    class ElementSupprime systemeClass

    %% ============================================
    %% NOTES
    %% ============================================

    note right of Utilisateur : **Roles :**\n• admin\n• medecin\n• infirmier\n• technicien

    note right of Document : **IA integree :**\n• OCR automatique\n• Classification\n• Analyse qualite

    note right of Rapport : **Workflow :**\n1. Brouillon\n2. Revision\n3. Validation\n4. Approbation

    note right of Activite : **Tracabilite :**\n• 20 actions\n• Audit trail\n• Logs IP/timestamp

    note right of ElementSupprime : **Suppression douce :**\n• Sauvegarde auto\n• Codes recuperation\n• Restauration 1 clic
```

## **Diagramme de Classe - Plateforme Médicale AL GHASSANI**

### **Architecture :**

#### **Utilisateurs**
- **Utilisateur** : Authentification, rôles, permissions
- **ProfilUtilisateur** : Extensions (avatar, bio, spécialisations)

#### **Patients**
- **Patient** : Dossier médical complet
- **DocumentPatient** : Documents joints (legacy)

#### **Documents IA**
- **Document** : OCR, classification automatique
- **TagDocument** : Système de tags
- **RelationTagDocument** : Association document-tag

#### **Rapports**
- **Rapport** : Workflow validation médicale
- **ModeleRapport** : Templates prédéfinis
- **CommentaireRapport** : Annotations

#### **Traçabilité**
- **Activite** : Logs complets des actions
- **ElementSupprime** : Suppression douce

---

## **Relations :**

```
Utilisateur (1) ─── (N) Document : cree
Utilisateur (1) ─── (N) Rapport : cree
Utilisateur (1) ─── (N) Patient : cree
Utilisateur (1) ─── (N) Activite : actions

Patient (1) ─── (N) Document : medical
Patient (1) ─── (N) Rapport : medical

Document (1) ─── (N) Tag : classification
Rapport (1) ─── (N) Commentaire : annotations
```

---

## **Méthodes principales :**

### **Utilisateur :**
- `get_full_name()` : Nom complet
- `has_permission()` : Vérification droits

### **Patient :**
- `get_age()` : Calcul âge
- `get_documents_count()` : Nombre documents

### **Document :**
- `is_urgent()` : Vérification urgence
- `get_quality_display()` : Qualité

### **Rapport :**
- `is_urgent()` : Vérification urgence
- `get_ai_confidence_display()` : Confiance IA

---

**Diagramme Mermaid simplifié et fonctionnel !**
