# Kindom - Plateforme de Kinésithérapie à Domicile

Kindom est une plateforme web permettant de mettre en relation des patients avec des kinésithérapeutes à domicile, ainsi que d'acheter du matériel de kinésithérapie.

## Fonctionnalités principales

- Gestion des rendez-vous avec des kinésithérapeutes à domicile
- Boutique en ligne de matériel de kinésithérapie
- Blog avec conseils médicaux
- Système d'évaluation et d'avis
- Gestion des profils utilisateurs

## Types d'utilisateurs

1. Visiteur
   - Consultation du site
   - Création de compte

2. Patient
   - Gestion des rendez-vous
   - Achat de matériel
   - Évaluation des services

3. Kinésithérapeute
   - Gestion des rendez-vous
   - Publication de conseils
   - Gestion du profil

4. Vendeur
   - Gestion de la boutique
   - Gestion des commandes

5. Administrateur
   - Gestion des comptes
   - Statistiques du site

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd kindom
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement
```bash
python manage.py runserver
```

## Technologies utilisées

- Django 5.1
- Python 3.11+
- Bootstrap 5
- SQLite (développement) / PostgreSQL (production)
- Pillow pour la gestion des images
- django-crispy-forms pour les formulaires
- django-allauth pour l'authentification

## Structure du projet

```
kindom/
├── accounts/          # Gestion des utilisateurs
├── appointments/      # Gestion des rendez-vous
├── shop/             # Boutique en ligne
├── blog/             # Articles et conseils
├── static/           # Fichiers statiques
├── media/            # Fichiers uploadés
└── templates/        # Templates HTML
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails. #   k i n e e d o m  
                           #   k i n e e 1 d o m  
 #   k i n e e 1 d o m m  
 #   k i n e d o m 1  
 #   k i e e d o m 1 1  
 #   k i e e d o m 1 1  
 #   k i n e e e d o m 1 1  
 #   k i n e l a s t  
 #   k i n e l a s t  
 #   k i n e l a s t  
 #   m e r k i n e  
 #   m e r k i n e 2  
 #   m e r k i n e 3  
 #   m e r k i n e e 3  
 