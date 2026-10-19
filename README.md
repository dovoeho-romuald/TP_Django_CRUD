# PROG1397 — TP Django CRUD : inventaire de capteurs IdO

Auteur : DOVOEHO

Application Django 5.2 (projet `inventaire_iot`, application `capteurs`) pour consulter, rechercher, créer, modifier et supprimer des fiches de capteurs.

## Installation (Windows, PowerShell)

Depuis le dossier du projet (celui qui contient `manage.py`) :

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

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

## Tests (scénarios 11 et 12)

```
.venv\Scripts\python.exe manage.py test capteurs -v 2
```

Les tests utilisent une base temporaire séparée : les fiches de travail ne sont pas modifiées.

## Contenu de l'archive

- `inventaire_iot/`, `capteurs/` (code, migrations, gabarits dans `capteurs/templates/capteurs/`, tests)
- `requirements.txt`, `README.md`
- `OBSERVATIONS.md` : les 12 scénarios de vérification
- `REPONSES.md` : les 6 questions de compréhension
- `captures/` : liste avec recherche, fiche détaillée, formulaire invalide, confirmation de suppression, sortie des tests
