# PROG1397 — TP Django CRUD : inventaire de capteurs IdO

Auteur : DOVOEHO

Application Django 5.2 (projet `inventaire_iot`, application `capteurs`) pour consulter, rechercher, créer, modifier et supprimer des fiches de capteurs.

## Installation (Windows, PowerShell)

Depuis le dossier du projet (celui qui contient `manage.py`) :

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Clé secrète (fichier .env)

La `SECRET_KEY` de Django n'est pas dans le code : elle est lue dans un fichier `.env` (non versionné, ignoré par `.gitignore`). Avant le premier lancement :

1. Copier le modèle : `Copy-Item .env.example .env`
2. Générer une clé :
   ```
   .venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. Coller cette clé dans `.env` à la place de `remplacer-par-une-cle-secrete`.

Sans ce fichier, Django s'arrête avec `KeyError: 'DJANGO_SECRET_KEY'`.

## Migrations

La base `db.sqlite3` n'est pas incluse dans l'archive. Pour la recréer :

```
.venv\Scripts\python.exe manage.py migrate
```

## Préparation des trois fiches

Ouvrir le shell Django :

```
.venv\Scripts\python.exe manage.py shell
```

Puis taper :

```python
from capteurs.models import Capteur
Capteur.objects.create(nom="Temp-Serre", type_capteur="T", emplacement="Serre A", actif=True, description="Surveillance de la serre")
Capteur.objects.create(nom="Hum-Atelier", type_capteur="H", emplacement="Atelier", actif=True, description="Contrôle de l'humidité")
Capteur.objects.create(nom="Press-Salle", type_capteur="P", emplacement="Salle N362", actif=False, description="Capteur retiré temporairement")
exit()
```

Autre possibilité : créer un superutilisateur (`manage.py createsuperuser`) et saisir les fiches dans http://127.0.0.1:8000/admin/.

## Démarrage

```
.venv\Scripts\python.exe manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/capteurs/ (la racine `/` retourne 404, c'est normal).

## Routes

| Chemin | Nom de route | GET | POST |
|---|---|---|---|
| `/capteurs/` | `capteurs:liste` | Liste + recherche | — |
| `/capteurs/<pk>/` | `capteurs:detail` | Fiche | — |
| `/capteurs/ajouter/` | `capteurs:ajouter` | Formulaire vide | Création |
| `/capteurs/<pk>/modifier/` | `capteurs:modifier` | Formulaire prérempli | Mise à jour |
| `/capteurs/<pk>/supprimer/` | `capteurs:supprimer` | Confirmation | Suppression |

## API REST (branche `capteurs-API`)

Construite avec Django REST Framework. CRUD complet sur les capteurs (voir « Méthodes acceptées »); les endpoints de catégorie sont en lecture seule. Les réponses sont en JSON; ouvertes dans un navigateur, elles s'affichent dans l'interface navigable de DRF.

| Endpoint (lecture GET) | Résultat |
|---|---|
| `/api/capteurs/` | Tous les capteurs, triés par nom |
| `/api/capteurs/<pk>/` | Un capteur (404 si l'ID n'existe pas) |
| `/api/capteurs/temperature/` | Capteurs de la catégorie Température (`T`) |
| `/api/capteurs/humidite/` | Capteurs de la catégorie Humidité (`H`) |
| `/api/capteurs/pression/` | Capteurs de la catégorie Pression (`P`) |

Exemple de réponse pour un capteur :

```json
{
    "id": 1,
    "nom": "Temp-Serre",
    "type_capteur": "T",
    "type_libelle": "Température",
    "emplacement": "Serre A",
    "actif": true,
    "description": "Surveillance de la serre"
}
```

Fichiers concernés : `capteurs/serializers.py` (`CapteurSerializer`), les vues `api_*` à la fin de `capteurs/views.py`, et les routes `api/` dans `inventaire_iot/urls.py`.

### Méthodes acceptées

| Endpoint | Méthodes | Réponses |
|---|---|---|
| `/api/capteurs/` | GET (lire), POST (créer) | 200, 201, 400 |
| `/api/capteurs/<pk>/` | GET (lire), PUT (modifier tout), PATCH (modifier une partie), DELETE (supprimer) | 200, 204, 400, 404 |
| `/api/capteurs/temperature/`, `/humidite/`, `/pression/` | GET seulement | 200 (autre méthode : 405) |

### Tests avec Postman

Le fichier `API_Capteurs_IdO.postman_collection.json` contient les 12 requêtes de test (GET, POST, PUT, PATCH, DELETE, cas d'erreur 400, 404 et 405).

1. Lancer le serveur : `.venv\Scripts\python.exe manage.py runserver`
2. Dans Postman : **Import**, puis choisir le fichier `API_Capteurs_IdO.postman_collection.json`.
3. Exécuter les requêtes dans l'ordre (01 à 12). La requête 07 (POST) mémorise l'id du capteur créé; les requêtes 09 à 11 (PUT, PATCH, DELETE) l'utilisent.

## Tests (scénarios 11 et 12)

```
.venv\Scripts\python.exe manage.py test capteurs -v 2
```

Les tests utilisent une base temporaire séparée : les fiches de travail ne sont pas modifiées.

## Contenu du dépôt

- `inventaire_iot/`, `capteurs/` (code, migrations, gabarits dans `capteurs/templates/capteurs/`, tests, API)
- `requirements.txt`, `README.md`, `.env.example` (modèle du fichier `.env`), `.gitignore`
- `OBSERVATIONS.md` : les 12 scénarios de vérification
- `REPONSES.md` : les 6 questions de compréhension
- `captures/` : liste avec recherche, fiche détaillée, formulaire invalide, confirmation de suppression, sortie des tests
