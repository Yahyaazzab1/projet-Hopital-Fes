# Description des Diagrammes de Cas d'Utilisation

## Diagramme de Cas d'Utilisation - Administrateur

Ce diagramme illustre les interactions de l'acteur principal "Administrateur" avec les différentes fonctionnalités du système. L'administrateur dispose de plusieurs modules principaux : la gestion des utilisateurs (création, modification, suppression de comptes et gestion des rôles), la gestion des patients (création, modification, visualisation, suppression), la gestion des médecins (modification, visualisation, suppression - les médecins étant importés via Excel), la gestion des infirmiers (création, modification, visualisation, suppression), la gestion des documents (création avec numérisation OCR, traitement IA, modification, visualisation, suppression), la gestion des rapports (création, modification, visualisation, validation, suppression), et la gestion des systèmes (configuration, consultation des logs, sauvegarde, audit). Les relations include montrent que toutes les actions nécessitent obligatoirement une connexion préalable, tandis que les relations extend représentent les fonctionnalités optionnelles qui peuvent être utilisées selon les besoins. L'administrateur a ainsi un accès complet et centralisé à toutes les fonctionnalités de gestion et de supervision du système hospitalier, avec notamment la capacité de traiter et numériser les documents médicaux avec des technologies d'intelligence artificielle.

---

## Diagramme de Cas d'Utilisation - Médecin

Ce diagramme illustre les interactions de l'acteur principal "Médecin" avec les différentes fonctionnalités du système de numérisation des dossiers médicaux. Le médecin dispose de trois modules principaux : la gestion des patients (création, modification, visualisation et recherche de dossiers patients), la gestion des documents médicaux (création, numérisation avec reconnaissance de caractères OCR, traitement par intelligence artificielle pour l'extraction de données, modification, visualisation et classification), et la gestion des rapports médicaux (création, modification, visualisation, soumission pour révision, validation, génération d'insights par IA, et exportation). Les relations include montrent que la connexion est obligatoire pour accéder aux fonctionnalités, et que la numérisation et le traitement IA sont intégrés dans le processus de création de documents. Les relations extend représentent les actions optionnelles selon les besoins cliniques. Le médecin se concentre ainsi sur ses fonctions essentielles de prise en charge des patients et de production de documents médicaux numérisés, bénéficiant de l'assistance de l'intelligence artificielle pour optimiser la qualité et la traçabilité des dossiers médicaux.

---

## Diagramme de Cas d'Utilisation - Infirmier

Ce diagramme illustre les interactions de l'acteur principal "Infirmier" avec les différentes fonctionnalités du système de numérisation des dossiers médicaux. L'infirmier dispose de trois modules principaux : la gestion des patients (visualisation des informations, recherche dans les dossiers et consultation complète des dossiers patients), la gestion des documents médicaux (visualisation, recherche, modification de documents existants et téléchargement), et la gestion des rapports médicaux (visualisation, recherche, exportation et consultation de l'historique). Les relations include montrent que la connexion est obligatoire pour accéder aux modules, tandis que les relations extend représentent les fonctionnalités optionnelles qui peuvent être utilisées selon les besoins. L'infirmier a un accès en lecture privilégié pour consulter et suivre les dossiers médicaux des patients, avec des droits limités sur l'édition des documents existants, et ne pouvant pas créer de nouveaux patients, documents ou rapports. Ce rôle est ainsi focalisé sur la consultation et le suivi des dossiers pour assister les médecins dans leurs activités quotidiennes.



