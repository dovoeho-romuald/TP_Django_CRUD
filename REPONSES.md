# Réponses aux questions de compréhension

Auteur : DOVOEHO

## 1. Routes et opérations CRUD

| Route | CRUD | Méthode qui modifie |
|---|---|---|
| `capteurs:liste` (`/capteurs/`) | R | aucune, seulement GET |
| `capteurs:detail` (`/capteurs/<pk>/`) | R | aucune, seulement GET |
| `capteurs:ajouter` (`/capteurs/ajouter/`) | C | POST |
| `capteurs:modifier` (`/capteurs/<pk>/modifier/`) | U | POST |
| `capteurs:supprimer` (`/capteurs/<pk>/supprimer/`) | D | POST |

La liste et la fiche servent juste à lire, donc elles n'ont pas besoin de POST. Même la recherche se fait en GET parce qu'elle filtre l'affichage mais ne change rien dans la base. Pour ajouter, modifier et supprimer, j'utilise POST parce que ça change les données. Pour ces trois routes, le GET affiche seulement une page (formulaire ou confirmation).

## 2. Différence entre Form et ModelForm

Pour la recherche, j'ai fait `RechercheCapteurForm` avec `forms.Form`. J'ai dû écrire moi-même les deux champs (`q` et `actifs_seulement`). Ce formulaire n'est pas relié au modèle et il n'enregistre rien, il sert juste à savoir quoi chercher.

Pour ajouter et modifier un capteur, j'ai fait `CapteurForm` avec `forms.ModelForm`. Là je n'ai pas écrit les champs : j'ai juste mis `model = Capteur` et la liste des champs dans `Meta`, et Django a créé le formulaire tout seul à partir du modèle. Il reprend aussi les règles du modèle, par exemple le nom unique et d'au moins 3 caractères. J'ai pu le voir quand j'ai essayé « AB » : l'erreur est apparue sans que j'écrive de code de validation. En plus, un ModelForm a la méthode `save()` qui enregistre le capteur dans la base.

## 3. Rôles de is_valid() et cleaned_data

`is_valid()` vérifie si les données envoyées respectent les règles (longueur, champ obligatoire, nom unique…). Ça retourne True ou False, et s'il y a des erreurs, elles sont gardées dans le formulaire pour être affichées dans la page.

`cleaned_data` contient les données une fois vérifiées et converties dans le bon type. Par exemple, la case « actifs seulement » devient `True` ou `False` au lieu du texte `"on"`. On peut utiliser `cleaned_data` seulement après avoir appelé `is_valid()`. C'est pour ça que dans ma vue `capteur_liste`, je lis `cleaned_data` seulement à l'intérieur du `if form.is_valid():`.

## 4. Où intervient instance pour la modification

Dans `capteur_modifier`, je vais d'abord chercher le capteur avec `get_object_or_404(Capteur, pk=pk)`.

- En GET, je fais `CapteurForm(instance=capteur)`. Ça remplit le formulaire avec les valeurs actuelles du capteur, comme ça l'utilisateur voit ce qu'il modifie.
- En POST, je fais `CapteurForm(request.POST, instance=capteur)`. Le formulaire prend les nouvelles valeurs envoyées, mais il sait qu'il doit les mettre dans ce capteur-là. Quand j'appelle `save()`, ça modifie le capteur existant et il garde le même pk.

Si on oublie `instance` dans le POST, `save()` va créer un nouveau capteur au lieu de modifier l'ancien. Et si on n'a pas changé le nom, on aurait une erreur « existe déjà », parce que le nom doit être unique.

## 5. Confirmation, POST, CSRF et autorisation

- **Confirmation :** quand on clique sur « Supprimer », ça n'efface rien tout de suite. Ça ouvre une page qui montre le nom du capteur et demande de confirmer. Ça évite de supprimer par erreur.
- **POST :** la suppression se fait seulement quand on clique sur le bouton « Confirmer la suppression », qui envoie un POST. Un lien fait toujours un GET, et un GET peut être ouvert sans le vouloir (un clic de trop, un robot, le navigateur qui précharge une page). Donc un GET ne doit jamais supprimer quelque chose.
- **CSRF :** le `{% csrf_token %}` ajoute un code caché dans le formulaire. Django vérifie ce code pour être sûr que la demande vient bien de mon site et pas d'un autre site qui essaierait d'envoyer la requête à ma place. Sans le code, Django répond 403. Je l'ai vérifié avec les tests (scénario 11).
- **Autorisation :** rien de tout ça ne vérifie qui a le droit de supprimer. N'importe qui qui ouvre la page peut confirmer. Pour vraiment protéger, il faudrait des comptes utilisateurs et une connexion obligatoire, mais ce n'était pas demandé dans ce TP.

## 6. Une erreur rencontrée

**L'erreur :** à l'étape 1, quand je cliquais sur un capteur dans la liste, j'avais l'erreur `TemplateDoesNotExist: capteurs/capteur_detail.html`. La liste marchait, mais pas la fiche.

**La cause :** en créant le fichier, je l'avais appelé `capteur.detail.html` avec un point, alors que dans ma vue j'avais écrit `capteur_detail.html` avec un tiret bas. Django cherche exactement le nom écrit dans `render()`, alors il ne trouvait pas le fichier.

**La correction :** j'ai renommé le fichier en `capteur_detail.html`.

**La preuve :** après le renommage, les fiches `/capteurs/1/`, `/capteurs/2/` et `/capteurs/3/` s'affichent (code 200), et `/capteurs/999/` donne toujours une 404 comme prévu.

J'ai aussi eu d'autres erreurs pendant le TP :
- `no such table: auth_user` : j'ai lancé `createsuperuser` avant `migrate`. J'ai compris qu'il faut d'abord faire `makemigrations` et `migrate` pour que les tables existent.
- Une erreur 500 sur Ajouter et Modifier : j'avais effacé par erreur `</form>` et `{% endblock %}` à la fin de `capteur_form.html`. Je les ai remis.
- Le titre affichait « Modifier AB » après une modification invalide, même si rien n'était enregistré. C'est parce que `is_valid()` met les valeurs dans l'objet en mémoire. J'ai corrigé en calculant le titre avant de créer le formulaire.
