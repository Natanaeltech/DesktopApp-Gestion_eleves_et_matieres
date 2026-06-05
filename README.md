# Gestion des matières et étudiants – Application Desktop

Application de gestion personnelle des matières (coefficients) et des étudiants (âge, sexe, filière, grade).  
Développée avec **PyQt6** pour l’interface, **SQLModel** pour l’ORM, **MySQL** pour la base de données, et **JWT** pour l’authentification.

## Fonctionnalités

-  **Authentification** : inscription / connexion avec JWT (token stocké en mémoire, blacklist à la déconnexion).
-  **Gestion des matières** : ajout, modification, suppression, liste.  
  Chaque matière possède un nom, une matière (ex: mathématiques) et un coefficient (entier ≥1).
-  **Gestion des étudiants** : ajout, modification, suppression, liste.  
  Chaque étudiant possède un nom, un âge (0‑120), un sexe (M/F), une filière (DSI/RMI) et un grade (L1 à M2).
-  **Propriétaire** : chaque utilisateur ne voit et ne modifie que ses propres données.
-  **Interface moderne** : thème sombre personnalisé, icônes (utilisation de `QIcon.fromTheme` ou fichiers locaux).

## Architecture du projet
Le projet suit une architecture multi‑tiers. Le dossier `src/` contient toute la logique métier : les modèles SQLModel (utilisateur, matière, étudiant, token), les schémas Pydantic pour la validation, les services (authentification, utilisateur, matière, étudiant), la dépendance `get_current_user` et un gestionnaire de session JWT global. Le dossier `gui/` regroupe les interfaces PyQt6 : fenêtres de connexion, d’inscription, fenêtre principale, onglets Matières et Étudiants, ainsi qu’une feuille de style QSS. À la racine se trouvent le point d’entrée `main.py`, la configuration de la base de données (`database.py`), les variables d’environnement (`config.py` et `.env`), et un script optionnel de création des tables.



## Prérequis

- Python 3.10 ou supérieur
- MySQL (serveur local ou distant)
- Environnement virtuel (recommandé)

## Installation

```bash
# 1. Cloner ou créer le dossier
mkdir mon_app_desktop && cd mon_app_desktop

# 2. Créer et activer l’environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
# DesktopApp-Gestion_eleves_et_matieres
