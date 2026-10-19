# Observations — les 12 scénarios de vérification

Auteur : DOVOEHO. Scénarios effectués dans l'ordre de l'énoncé, sur la base de travail (sauf 11 et 12 : base de test séparée).

| # | Manipulation | Résultat attendu | Résultat observé | Statut |
|---|---|---|---|---|
| 1 | Afficher la liste et les fiches initiales | 3 capteurs; champs lisibles; navigation complète | 3 capteurs triés par nom. Type affiché « Température / Humidité / Pression », actif « Oui/Non ». Chaque nom ouvre sa fiche (5 champs), lien « Retour à la liste » fonctionnel. Pages en code 200. | Réussi |
| 2 | Consulter un ID absent | 404, sans modification | `/capteurs/999/` → page 404 « Not Found ». Total toujours 3. | Réussi |
| 3 | Rechercher « Serre » puis « actifs seulement » | 1 résultat, puis 2 actifs; total en base toujours 3 | `?q=Serre` → Temp-Serre seulement. Case cochée → Hum-Atelier et Temp-Serre. Total en base : 3. | Réussi |
| 4 | Rechercher un nom absent | Message « Aucun capteur »; aucune écriture | `?q=xyz` → « Aucun capteur. ». Total : 3. Une recherche de plus de 40 caractères (via l'URL) affiche l'erreur de validation et aucun résultat. | Réussi |
| 5 | Créer Temp-Bureau correctement | Redirection vers sa fiche; total 4 | Après « Enregistrer », redirection vers `/capteurs/4/`. Total : 4. (Créé d'abord en minuscules « temp-bureau », corrigé à l'étape de modification.) | Réussi |
| 6 | Créer le même nom; nom de 2 caractères; emplacement vide | Erreurs visibles; saisie conservée; total 4 | Nom en double → « existe déjà ». « AB » → « at least 3 characters ». Emplacement vide → bloqué par le navigateur (attribut `required`); vérifié côté serveur avec le client de test : erreur sur le champ et saisie conservée. Le formulaire reste rempli. Total : 4. | Réussi |
| 7 | Ouvrir Modifier puis enregistrer emplacement et actif=False | Préremplissage; même pk; total 4 | Formulaire prérempli. Enregistré : nom « Temp-Bureau », emplacement « Bureau enseignant », actif Non. Redirection vers `/capteurs/4/` (même pk). Total : 4. | Réussi |
| 8 | Envoyer une modification invalide | Erreurs; aucune modification persistante | Nom « AB » → erreur affichée. En base, le nom reste « Temp-Bureau ». Défaut corrigé : le titre affichait « Modifier AB » (voir REPONSES.md, question 6). | Réussi |
| 9 | Ouvrir la confirmation puis Annuler | Capteur présent; total 4 | La page de confirmation s'affiche (GET) sans rien supprimer. « Annuler » ramène à la fiche. Total : 4. | Réussi |
| 10 | Confirmer la suppression | Redirection liste; total 3; ancienne fiche 404 | Après « Confirmer la suppression » → redirection vers la liste, 3 capteurs. `/capteurs/4/` → 404. | Réussi |
| 11 | POST sans CSRF avec `Client(enforce_csrf_checks=True)` | 403; aucune création/modification/suppression | 3 tests (ajouter, modifier, supprimer) : réponse 403 et base inchangée. Voir `captures/5_tests_scenarios_11_12.txt`. | Réussi |
| 12 | Liste vide dans une base de test distincte | Message clair; lien Ajouter toujours présent | Test `test_liste_vide` : code 200, « Aucun capteur » et lien vers `/capteurs/ajouter/` présents. Fiches de travail non touchées. | Réussi |

Commande des tests : `.venv\Scripts\python.exe manage.py test capteurs -v 2` → `Ran 4 tests ... OK`.
