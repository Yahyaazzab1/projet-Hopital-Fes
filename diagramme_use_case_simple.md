```mermaid
graph TD
    %% ============================================
    %% ACTEURS DU SYSTÈME
    %% ============================================

    %% Acteurs principaux
    Admin[Administrateur<br/>Gestion complete]
    Doctor[Medecin<br/>Soins medicaux]
    Nurse[Infirmier<br/>Soins quotidiens]
    System[Systeme AL GHASSANI<br/>Plateforme medicale IA]

    %% ============================================
    %% CAS D'USAGE - AUTHENTIFICATION
    %% ============================================

    %% Connexion/Déconnexion (tous les acteurs)
    Admin --> UC1[Authentification]
    Doctor --> UC1
    Nurse --> UC1

    UC1 --> UC2[Deconnexion]
    UC1 --> UC3[Gerer profil]

    %% ============================================
    %% CAS D'USAGE - ADMINISTRATION (ADMIN SEULEMENT)
    %% ============================================

    Admin --> UC10[Gerer utilisateurs]
    Admin --> UC11[Configurer systeme]
    Admin --> UC12[Superviser activite]
    Admin --> UC13[Gerer sauvegardes]
    Admin --> UC14[Consulter audit]
    Admin --> UC15[Restaurer donnees]

    %% ============================================
    %% CAS D'USAGE - GESTION PATIENTS (ADMIN + DOCTOR)
    %% ============================================

    Admin --> UC20[Creer patient]
    Doctor --> UC20
    Admin --> UC21[Consulter patient]
    Doctor --> UC21
    Nurse --> UC21
    Admin --> UC22[Modifier patient]
    Doctor --> UC22
    Admin --> UC23[Rechercher patients]
    Doctor --> UC23
    Nurse --> UC23

    %% ============================================
    %% CAS D'USAGE - DOCUMENTS MÉDICAUX (ADMIN + DOCTOR + NURSE)
    %% ============================================

    Admin --> UC30[Importer document]
    Doctor --> UC30
    Admin --> UC31[Traiter document IA]
    Doctor --> UC31
    Admin --> UC32[Classifier document]
    Doctor --> UC32
    Admin --> UC33[Consulter documents]
    Doctor --> UC33
    Nurse --> UC33
    Admin --> UC34[Modifier document]
    Doctor --> UC34
    Nurse --> UC34
    Admin --> UC35[Rechercher documents]
    Doctor --> UC35
    Nurse --> UC35

    %% ============================================
    %% CAS D'USAGE - RAPPORTS MÉDICAUX (ADMIN + DOCTOR + NURSE)
    %% ============================================

    Admin --> UC40[Creer rapport]
    Doctor --> UC40
    Admin --> UC41[Soumettre revision]
    Doctor --> UC41
    Admin --> UC42[Valider rapport]
    Doctor --> UC42
    Admin --> UC43[Consulter rapports]
    Doctor --> UC43
    Nurse --> UC43
    Admin --> UC44[Commenter rapport]
    Doctor --> UC44
    Admin --> UC45[Generer insights IA]
    Doctor --> UC45
    Admin --> UC46[Exporter rapport]
    Doctor --> UC46
    Nurse --> UC46

    %% ============================================
    %% CAS D'USAGE - TÂCHES ET PLANNING (DOCTOR + NURSE)
    %% ============================================

    Doctor --> UC50[Creer tache]
    Nurse --> UC50
    Doctor --> UC51[Consulter planning]
    Nurse --> UC51
    Doctor --> UC52[Suivre execution]
    Nurse --> UC52
    Doctor --> UC53[Marquer terminee]
    Nurse --> UC53

    %% ============================================
    %% CAS D'USAGE - SYSTÈME ET OUTILS (TOUS)
    %% ============================================

    Admin --> UC60[Scanner QR codes]
    Doctor --> UC60
    Nurse --> UC60

    Admin --> UC61[Consulter statistiques]
    Doctor --> UC61
    Nurse --> UC61

    Admin --> UC62[Recevoir notifications]
    Doctor --> UC62
    Nurse --> UC62

    %% ============================================
    %% RELATIONS ENTRE CAS D'USAGE
    %% ============================================

    UC1 --> UC3
    UC3 --> UC2

    UC20 --> UC21
    UC21 --> UC22
    UC21 --> UC23
    UC22 --> UC21
    UC23 --> UC21

    UC30 --> UC31
    UC31 --> UC32
    UC32 --> UC33
    UC33 --> UC34
    UC33 --> UC35
    UC34 --> UC33
    UC35 --> UC33

    UC40 --> UC41
    UC41 --> UC42
    UC42 --> UC43
    UC43 --> UC44
    UC43 --> UC45
    UC43 --> UC46
    UC44 --> UC43
    UC45 --> UC43
    UC46 --> UC43

    UC50 --> UC51
    UC51 --> UC52
    UC52 --> UC53
    UC53 --> UC51

    %% ============================================
    %% CONFIGURATION VISUELLE
    %% ============================================

    %% Styles pour les acteurs
    classDef acteurAdmin fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef acteurDoctor fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef acteurNurse fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef systemClass fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000

    class Admin acteurAdmin
    class Doctor acteurDoctor
    class Nurse acteurNurse
    class System systemClass

    %% Styles pour les cas d'usage par rôle
    classDef ucAdmin fill:#e1f5fe,stroke:#01579b,stroke-width:1px,color:#000
    classDef ucMedical fill:#f3e5f5,stroke:#4a148c,stroke-width:1px,color:#000
    classDef ucDocument fill:#e8f5e8,stroke:#1b5e20,stroke-width:1px,color:#000
    classDef ucReport fill:#fff3e0,stroke:#e65100,stroke-width:1px,color:#000
    classDef ucTask fill:#fce4ec,stroke:#880e4f,stroke-width:1px,color:#000
    classDef ucSystem fill:#f5f5f5,stroke:#424242,stroke-width:1px,color:#000

    %% Application des styles aux cas d'usage
    class UC1,UC2,UC3,UC10,UC11,UC12,UC13,UC14,UC15 ucAdmin
    class UC20,UC21,UC22,UC23,UC60,UC61,UC62 ucMedical
    class UC30,UC31,UC32,UC33,UC34,UC35 ucDocument
    class UC40,UC41,UC42,UC43,UC44,UC45,UC46 ucReport
    class UC50,UC51,UC52,UC53 ucTask

    %% ============================================
    %% NOTES ET LÉGENDES
    %% ============================================

    note right of Admin : **Administrateur**\n- Gestion complete systeme\n- Administration utilisateurs\n- Configuration et audit\n- Supervision globale

    note right of Doctor : **Medecin**\n- Gestion patients complete\n- Documents et rapports\n- Taches et planning\n- Validation medicale

    note right of Nurse : **Infirmier**\n- Consultation patients\n- Visualisation documents\n- Suivi taches journalieres\n- Actions sur documents

    note right of System : **Systeme AL GHASSANI**\n- Plateforme medicale IA\n- Tracabilite complete\n- Conformite legale\n- Securite d'entreprise

    %% Légende simplifiée
    subgraph "Legende"
        direction TB
        A[Admin uniquement]
        B[Admin + Medecin]
        C[Tous les roles]
        D[Documents medicaux]
        E[Rapports medicaux]
        F[Taches et planning]
    end

    %% Styles pour la légende
    classDef legendClass fill:#ffffff,stroke:#ddd,stroke-width:1px,color:#000
    class A,B,C,D,E,F legendClass
```

## **Diagramme de Cas d'Usage - Plateforme Médicale AL GHASSANI**

### **Vue d'ensemble du système**

La plateforme **AL GHASSANI** organise ses fonctionnalités autour de **trois acteurs principaux** avec des **permissions différenciées** selon les rôles médicaux. Le système gère **l'ensemble du workflow hospitalier** depuis l'authentification jusqu'aux rapports médicaux validés.

---

## **1. ACTEURS DU SYSTÈME**

### **Administrateur (Accès complet)**
- **Gestion système** : Configuration, utilisateurs, audit
- **Supervision** : Monitoring, sauvegardes, métriques
- **Conformité** : Traçabilité légale, sécurité

### **Médecin (Gestion médicale)**
- **Patients** : CRUD complet, recherche avancée
- **Documents** : Import, traitement IA, classification
- **Rapports** : Création, validation, export
- **Tâches** : Planification et suivi d'exécution

### **Infirmier (Consultation)**
- **Patients** : Consultation et recherche
- **Documents** : Visualisation et modification
- **Rapports** : Consultation et export
- **Tâches** : Suivi quotidien et completion

---

## **2. CAS D'USAGE PAR CATÉGORIE**

### **Authentification (Tous les acteurs)**
1. **Authentification** : Connexion sécurisée avec IP tracking
2. **Deconnexion** : Fermeture session avec log d'audit
3. **Gerer profil** : Informations personnelles et préférences

### **Administration (Admin uniquement)**
4. **Gerer utilisateurs** : CRUD comptes et rôles
5. **Configurer systeme** : Paramètres et maintenance
6. **Superviser activite** : Métriques et monitoring
7. **Gerer sauvegardes** : Automatique et manuelle
8. **Consulter audit** : Traçabilité complète
9. **Restaurer donnees** : Récupération depuis suppression douce

### **Gestion Patients (Admin + Médecin)**
10. **Créer patient** : Dossier médical complet
11. **Consulter patient** : Historique et informations
12. **Modifier patient** : Mise à jour des données
13. **Rechercher patients** : Filtres avancés

### **Documents Médicaux (Admin + Médecin + Infirmier)**
14. **Importer document** : Upload images/PDF médicaux
15. **Traiter document IA** : OCR automatique et extraction
16. **Classifier document** : Tags et catégories intelligentes
17. **Consulter documents** : Visualisation et métadonnées
18. **Modifier document** : Corrections et annotations
19. **Rechercher documents** : Full-text et filtres

### **Rapports Médicaux (Admin + Médecin + Infirmier)**
20. **Créer rapport** : Rédaction avec templates
21. **Soumettre revision** : Workflow de validation
22. **Valider rapport** : Approbation médicale/admin
23. **Consulter rapports** : Lecture et recherche
24. **Commenter rapport** : Annotations collaboratives
25. **Generer insights IA** : Analyse automatique
26. **Exporter rapport** : PDF et formats multiples

### **Tâches et Planning (Médecin + Infirmier)**
27. **Créer tache** : Planification des soins
28. **Consulter planning** : Vue d'ensemble des activités
29. **Suivre execution** : Statut temps réel
30. **Marquer terminee** : Validation des actions

### **Système et Outils (Tous les acteurs)**
31. **Scanner QR codes** : Identification patients/rapports
32. **Consulter statistiques** : Métriques personnalisées
33. **Recevoir notifications** : Alertes temps réel

---

## **3. WORKFLOWS PRINCIPAUX**

### **Workflow Patient :**
```
Création → Consultation → Modification → Recherche
     ↓
Documents médicaux → Rapports → Validation
```

### **Workflow Document :**
```
Import → Traitement IA → Classification → Consultation
    ↓                    ↓
Modification ← Recherche ← Consultation
```

### **Workflow Rapport :**
```
Création → Révision → Validation → Approbation → Publication
    ↓         ↓          ↓           ↓
Commentaires ← Insights IA ← Export ← Consultation
```

### **Workflow Tâche :**
```
Création → Planification → Exécution → Completion
    ↓           ↓            ↓
Consultation ← Suivi ← Consultation
```

---

## **4. FONCTIONNALITÉS TECHNIQUES**

### **Intelligence Artificielle :**
- **OCR automatique** pour extraction de texte médical
- **Classification intelligente** des documents
- **Génération d'insights** pour les rapports
- **Analyse de qualité** et scoring de confiance

### **Sécurité et Audit :**
- **Traçabilité complète** de toutes les actions
- **Permissions granulaires** par rôle
- **Logs détaillés** (IP, User-Agent, timestamp)
- **Suppression douce** avec récupération

### **Interface Utilisateur :**
- **Dashboards personnalisés** par rôle
- **Navigation intuitive** avec menus contextuels
- **Recherche full-text** et filtres avancés
- **Notifications temps réel** et alertes

---

## **5. MÉTRIQUES ET CONTRAINTES**

### **Performance :**
- **Temps de réponse** < 2 secondes pour recherches
- **Traitement IA** < 30 secondes par document
- **Workflow validation** < 24h pour rapports critiques
- **Disponibilité système** 99.9%

### **Conformité :**
- **Conservation données** selon réglementation médicale
- **Audit trail** complet pour inspections
- **Sécurité des accès** avec permissions granulaires
- **Traçabilité** des modifications médicales

---

**Diagramme de cas d'usage simplifié et fonctionnel pour plateforme médicale !**

**Représentation claire des workflows médicaux avec permissions et conformité légale.**

## 📋 **Diagramme de Cas d'Usage - Plateforme Médicale AL GHASSANI**

### 🏗️ **Vue d'ensemble du système**

La plateforme **AL GHASSANI** organise ses fonctionnalités autour de **trois acteurs principaux** avec des **permissions différenciées** selon les rôles médicaux. Le système gère **l'ensemble du workflow hospitalier** depuis l'authentification jusqu'aux rapports médicaux validés.

---

## 👥 **1. ACTEURS DU SYSTÈME**

### **👑 Administrateur (Accès complet)**
- **Gestion système** : Configuration, utilisateurs, audit
- **Supervision** : Monitoring, sauvegardes, métriques
- **Conformité** : Traçabilité légale, sécurité

### **👨‍⚕️ Médecin (Gestion médicale)**
- **Patients** : CRUD complet, recherche avancée
- **Documents** : Import, traitement IA, classification
- **Rapports** : Création, validation, export
- **Tâches** : Planification et suivi d'exécution

### **👩‍⚕️ Infirmier (Consultation)**
- **Patients** : Consultation et recherche
- **Documents** : Visualisation et modification
- **Rapports** : Consultation et export
- **Tâches** : Suivi quotidien et completion

---

## 📋 **2. CAS D'USAGE PAR CATÉGORIE**

### **🔐 Authentification (Tous les acteurs)**
1. **Authentification** : Connexion sécurisée avec IP tracking
2. **Deconnexion** : Fermeture session avec log d'audit
3. **Gerer profil** : Informations personnelles et préférences

### **👥 Administration (Admin uniquement)**
4. **Gerer utilisateurs** : CRUD comptes et rôles
5. **Configurer systeme** : Paramètres et maintenance
6. **Superviser activite** : Métriques et monitoring
7. **Gerer sauvegardes** : Automatique et manuelle
8. **Consulter audit** : Traçabilité complète
9. **Restaurer donnees** : Récupération depuis suppression douce

### **🏥 Gestion Patients (Admin + Médecin)**
10. **Créer patient** : Dossier médical complet
11. **Consulter patient** : Historique et informations
12. **Modifier patient** : Mise à jour des données
13. **Rechercher patients** : Filtres avancés

### **📄 Documents Médicaux (Admin + Médecin + Infirmier)**
14. **Importer document** : Upload images/PDF médicaux
15. **Traiter document IA** : OCR automatique et extraction
16. **Classifier document** : Tags et catégories intelligentes
17. **Consulter documents** : Visualisation et métadonnées
18. **Modifier document** : Corrections et annotations
19. **Rechercher documents** : Full-text et filtres

### **📊 Rapports Médicaux (Admin + Médecin + Infirmier)**
20. **Créer rapport** : Rédaction avec templates
21. **Soumettre revision** : Workflow de validation
22. **Valider rapport** : Approbation médicale/admin
23. **Consulter rapports** : Lecture et recherche
24. **Commenter rapport** : Annotations collaboratives
25. **Generer insights IA** : Analyse automatique
26. **Exporter rapport** : PDF et formats multiples

### **📅 Tâches et Planning (Médecin + Infirmier)**
27. **Créer tache** : Planification des soins
28. **Consulter planning** : Vue d'ensemble des activités
29. **Suivre execution** : Statut temps réel
30. **Marquer terminee** : Validation des actions

### **🛠️ Système et Outils (Tous les acteurs)**
31. **Scanner QR codes** : Identification patients/rapports
32. **Consulter statistiques** : Métriques personnalisées
33. **Recevoir notifications** : Alertes temps réel

---

## 🔄 **3. WORKFLOWS PRINCIPAUX**

### **🔄 Workflow Patient :**
```
Création → Consultation → Modification → Recherche
     ↓
Documents médicaux → Rapports → Validation
```

### **🔄 Workflow Document :**
```
Import → Traitement IA → Classification → Consultation
    ↓                    ↓
Modification ← Recherche ← Consultation
```

### **🔄 Workflow Rapport :**
```
Création → Révision → Validation → Approbation → Publication
    ↓         ↓          ↓           ↓
Commentaires ← Insights IA ← Export ← Consultation
```

### **🔄 Workflow Tâche :**
```
Création → Planification → Exécution → Completion
    ↓           ↓            ↓
Consultation ← Suivi ← Consultation
```

---

## 🎯 **4. FONCTIONNALITÉS TECHNIQUES**

### **🤖 Intelligence Artificielle :**
- **OCR automatique** pour extraction de texte médical
- **Classification intelligente** des documents
- **Génération d'insights** pour les rapports
- **Analyse de qualité** et scoring de confiance

### **🔐 Sécurité et Audit :**
- **Traçabilité complète** de toutes les actions
- **Permissions granulaires** par rôle
- **Logs détaillés** (IP, User-Agent, timestamp)
- **Suppression douce** avec récupération

### **📱 Interface Utilisateur :**
- **Dashboards personnalisés** par rôle
- **Navigation intuitive** avec menus contextuels
- **Recherche full-text** et filtres avancés
- **Notifications temps réel** et alertes

---

## 📊 **5. MÉTRIQUES ET CONTRAINTES**

### **Performance :**
- **Temps de réponse** < 2 secondes pour recherches
- **Traitement IA** < 30 secondes par document
- **Workflow validation** < 24h pour rapports critiques
- **Disponibilité système** 99.9%

### **Conformité :**
- **Conservation données** selon réglementation médicale
- **Audit trail** complet pour inspections
- **Sécurité des accès** avec permissions granulaires
- **Traçabilité** des modifications médicales

---

**🏥 Diagramme de cas d'usage simplifié et fonctionnel pour plateforme médicale !** 🏥✨

**Représentation claire des workflows médicaux avec permissions et conformité légale.** 🚀
