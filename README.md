# 🏥 Plateforme Médicale AL GHASSANI

> Solution complète de gestion hospitalière avec intelligence artificielle intégrée et traçabilité totale

[![Django](https://img.shields.io/badge/Django-4.2.24-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-7952B3?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Rôles et permissions](#-rôles-et-permissions)
- [API REST](#-api-rest)
- [Contribution](#-contribution)
- [Licence](#-licence)
- [Contact](#-contact)

## 🎯 À propos

La **Plateforme Médicale AL GHASSANI** est une application web complète développée pour l'hôpital AL GHASSANI à Fès, Maroc. Elle permet de gérer l'ensemble du workflow médical depuis l'accueil des patients jusqu'aux rapports médicaux validés, avec une intégration d'intelligence artificielle pour l'extraction et la classification automatique de documents médicaux.

### Objectifs principaux

- ✅ **Centralisation** des données médicales
- ✅ **Automatisation** des processus administratifs
- ✅ **Traçabilité** complète des actions médicales
- ✅ **Intelligence artificielle** pour l'analyse de documents
- ✅ **Interface intuitive** pour tous les rôles médicaux

## 🚀 Fonctionnalités

### 👥 Gestion des utilisateurs
- Authentification sécurisée avec gestion des rôles
- Profils utilisateurs étendus (avatar, bio, spécialisations)
- Historique des connexions avec tracking IP
- Permissions granulaires par rôle

### 🏥 Gestion des patients
- Dossier médical complet et sécurisé
- Recherche avancée par nom, CI, téléphone
- Historique des consultations et visites
- Gestion des statuts (actif/inactif/décédé/transféré)
- Export des données patient

### 📄 Documents médicaux intelligents
- Upload de documents (images, PDFs)
- **OCR automatique** pour extraction de texte
- **Classification intelligente** des documents
- Analyse de qualité avec score de confiance
- Recherche full-text dans le contenu
- Tagging automatique et indexation

### 📊 Rapports médicaux
- Création de rapports multi-types (consultation, urgence, chirurgie, etc.)
- Workflow de validation (brouillon → révision → validation)
- Commentaires administratifs et annotations
- Export PDF automatique
- Gestion des priorités et urgences

### 🖥️ Tableau de bord
- Vue d'ensemble avec statistiques temps réel
- Graphiques interactifs (Chart.js)
- Notifications et alertes
- Raccourcis vers les modules clés
- Dashboards personnalisés par rôle

### 📱 Numérisation / Scanner
- Interface de numérisation assistée
- Capture de documents via caméra
- Retouches de base (nettoyage, ajustements)
- Intégration directe dans le dossier patient

### 🔔 Notifications et alertes
- Système d'alertes pour validations en attente
- Notifications pour rapports urgents
- Historisation des notifications
- Alertes visuelles sur l'interface

### ⚙️ Administration
- Gestion des comptes utilisateurs
- Attribution de rôles et permissions
- Configuration des paramètres système
- Suivi des activités clés

### 🗑️ Corbeille logique (Soft Delete)
- Suppression réversible des entités
- Récupération des données supprimées
- Prévention de la perte accidentelle

## 🛠️ Technologies utilisées

### Backend
- **Python 3.x** - Langage de programmation principal
- **Django 4.2.24** - Framework web MVT
- **Django REST Framework** - API RESTful
- **django-cors-headers** - Gestion CORS
- **SQLite** - Base de données (développement)

### Frontend
- **HTML5** - Structure des pages
- **CSS3** - Stylisation et mise en page
- **JavaScript (ES6+)** - Interactivité côté client
- **Bootstrap 5.3.0** - Framework CSS responsive
- **Font Awesome 6.4.0** - Bibliothèque d'icônes
- **Chart.js** - Graphiques interactifs

### Technologies Web
- **WebRTC (getUserMedia API)** - Accès caméra pour scanner
- **Canvas API** - Traitement d'images
- **LocalStorage / SessionStorage** - Stockage client

### Outils de développement
- **Git** - Gestion de versions
- **PlantUML** - Diagrammes UML

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.8+** ([Télécharger Python](https://www.python.org/downloads/))
- **pip** (gestionnaire de paquets Python)
- **Git** ([Télécharger Git](https://git-scm.com/downloads))

## 🔧 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/projet-Hopital-Fes.git
cd projet-Hopital-Fes
```

### 2. Créer un environnement virtuel

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install django==4.2.24
pip install djangorestframework
pip install django-cors-headers
```

Ou créez un fichier `requirements.txt` :

```txt
Django==4.2.24
djangorestframework
django-cors-headers
```

Puis installez :

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

### 6. Collecter les fichiers statiques

```bash
python manage.py collectstatic
```

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8000/**

## ⚙️ Configuration

### Variables d'environnement

Pour la production, créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre-clé-secrète-ici
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuration de la base de données

Par défaut, le projet utilise SQLite. Pour utiliser PostgreSQL ou MySQL, modifiez `medical_backend/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nom_base_donnees',
        'USER': 'utilisateur',
        'PASSWORD': 'mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📖 Utilisation

### Accès à l'application

1. Ouvrez votre navigateur et accédez à **http://127.0.0.1:8000/**
2. Connectez-vous avec votre compte superutilisateur
3. Accédez au tableau de bord via **http://127.0.0.1:8000/dashboard/**

### Interface d'administration Django

L'interface d'administration Django est accessible à : **http://127.0.0.1:8000/admin/**

### Rôles disponibles

- **👑 Administrateur** : Accès complet à toutes les fonctionnalités
- **👨‍⚕️ Médecin** : Gestion des patients, documents et rapports
- **👩‍⚕️ Infirmier** : Consultation et modification (lecture seule pour création)
- **🔧 Technicien** : Maintenance et monitoring système

## 📁 Structure du projet

```
projet-Hopital-Fes/
│
├── medical_backend/          # Configuration Django principale
│   ├── settings.py           # Paramètres de l'application
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Configuration WSGI
│
├── medical/                  # Application principale
│   ├── models.py            # Modèles de données
│   ├── views.py              # Vues et logique métier
│   ├── urls.py               # URLs de l'application
│   └── utils.py              # Utilitaires et helpers
│
├── users/                    # Gestion des utilisateurs
│   ├── models.py            # Modèle User personnalisé
│   └── views.py              # Vues utilisateurs
│
├── patients/                 # Gestion des patients
│   ├── models.py            # Modèle Patient
│   ├── views.py              # Vues patients
│   └── serializers.py        # Sérialiseurs API
│
├── documents/                # Gestion des documents
│   ├── models.py            # Modèle Document
│   └── views.py              # Vues documents
│
├── reports/                  # Gestion des rapports
│   ├── models.py            # Modèle Report
│   └── views.py              # Vues rapports
│
├── settings/                 # Paramètres système
│   └── models.py            # Configuration établissement
│
├── templates/                # Templates HTML
│   ├── medical/             # Templates médicaux
│   ├── users/               # Templates utilisateurs
│   └── dashboard/           # Templates dashboard
│
├── static/                   # Fichiers statiques
│   ├── css/                 # Feuilles de style
│   ├── js/                  # Scripts JavaScript
│   └── img/                 # Images
│
├── media/                    # Fichiers média uploadés
│   └── documents/           # Documents médicaux
│
├── manage.py                 # Script de gestion Django
└── db.sqlite3               # Base de données SQLite
```

## 👥 Rôles et permissions

### Administrateur 👑
- ✅ Accès complet à toutes les fonctionnalités
- ✅ Gestion des utilisateurs et rôles
- ✅ Configuration système
- ✅ Audit et logs complets
- ✅ Maintenance et sauvegardes

### Médecin 👨‍⚕️
- ✅ CRUD complet patients
- ✅ Upload et modification documents
- ✅ Création et validation rapports
- ✅ Consultation historique médical
- ✅ Export des données médicales

### Infirmier 👩‍⚕️
- ✅ Consultation patients et dossiers
- ✅ Visualisation documents (lecture seule)
- ✅ Modification documents existants
- ✅ Tâches du jour et planning
- ❌ Création/Suppression interdite

### Technicien 🔧
- ✅ Monitoring système
- ✅ Logs et diagnostics
- ✅ Sauvegardes
- ✅ Maintenance
- ❌ Accès médical restreint

## 🔌 API REST

L'application expose une API REST complète pour toutes les entités principales.

### Endpoints disponibles

- **Patients** : `/api/patients/`
- **Documents** : `/api/documents/`
- **Rapports** : `/api/reports/`
- **Utilisateurs** : `/api/users/`

### Authentification API

L'API utilise l'authentification par token. Pour obtenir un token :

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "votre_username", "password": "votre_password"}'
```

### Exemple d'utilisation

```python
import requests

# Obtenir la liste des patients
response = requests.get(
    'http://127.0.0.1:8000/api/patients/',
    headers={'Authorization': 'Token votre_token_ici'}
)

patients = response.json()
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Guidelines de contribution

- Suivez les conventions de code Python (PEP 8)
- Ajoutez des tests pour les nouvelles fonctionnalités
- Documentez votre code
- Assurez-vous que tous les tests passent

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Contact

**Projet développé pour l'Hôpital AL GHASSANI - Fès, Maroc**

- 📧 Email : [votre-email@example.com](mailto:votre-email@example.com)
- 🌐 Site web : [votre-site.com](https://votre-site.com)
- 📱 Téléphone : +212 XXX XXX XXX

---

<div align="center">

**Fait avec ❤️ pour améliorer les soins médicaux**

[⬆ Retour en haut](#-plateforme-médicale-al-ghassani)

</div>

