# Interface Infirmier - Plateforme Médicale AL GHASSANI

## 1. Tableau de Bord

### Section Statistiques
- **Patients** : [Nombre total de patients assignés]
- **Documents en attente** : [Nombre de documents à traiter]
- **Rapports à compléter** : [Nombre de rapports en attente]
- **Tâches urgentes** : [Nombre de tâches prioritaires du jour]

### Actions Rapides
- Voir mes patients
- Consulter les alertes
- Saisir un soin
- Rédiger un rapport

---

## 2. Liste des Patients

### Filtres
- Par statut (Tous/En soins/Suivi/Urgent)
- Par service/étage
- Par médecin référent

### Liste
Pour chaque patient :
- Photo/Identité
- Âge/Chambre/Lit
- Statut (🟢 Stable /🟡 Suivi /🔴 Urgent)
- Dernière intervention
- Prochaine action requise

---

## 3. Dossier Patient

### Fiche d'identité (Lecture seule)
- Nom, Prénom, Âge
- N° dossier médical
- Médecin référent
- Allergies connues
- Groupe sanguin

### Constantes Vitales
- Formulaire de saisie avec champs :
  - Tension artérielle
  - Pouls
  - Température
  - Saturation O2
  - Glycémie
  - Échelle de douleur
  - Date/Heure
  - Signature électronique

### Historique des Soins
- Liste chronologique avec filtre par date
- Type de soin
- Infirmier en charge
- Observations

### Documents (Consultation seule)
- Ordonnances
- Comptes-rendus médicaux
- Examens biologiques
- Courbes de suivi

### Rapports Infirmiers
- Consultation des rapports existants
- Bouton "Nouveau rapport"
- Filtres par date/type

---

## 4. Gestion des Soins

### Planning des Soins
- Vue par jour/semaine
- Soins programmés avec statut :
  - ⏳ À faire
  - 🔄 En cours
  - ✅ Terminé
  - ❌ Reporté

### Fiche de Soins
- Type de soin (liste déroulante)
- Date/Heure de réalisation
- Observations
- Produits/matériels utilisés
- Signature électronique

### Alertes et Tâches
- Liste des alertes actives
- Tâches déléguées
- Rappels importants

---

## 5. Rapports et Transmission

### Nouveau Rapport
- Modèle de rapport pré-rempli
- Champs libres pour observations
- Liste de vérification
- Pièces jointes (photos, documents)
- Validation et signature

### Historique des Transmissions
- Recherche par date/patient
- Filtres par type de transmission
- Consultation des rapports archivés

### Exports
- Génération de PDF
- Impression des transmissions
- Export des données (si autorisé)

---

## 6. Paramètres et Profil

### Mon Profil
- Informations personnelles
- Photo de profil
- Coordonnées
- Horaires de travail

### Préférences
- Thème (clair/sombre)
- Notifications
- Langue

### Déconnexion
- Bouton de déconnexion visible
- Verrouillage d'écran rapide
