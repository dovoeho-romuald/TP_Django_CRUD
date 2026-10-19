from django.shortcuts import render, get_object_or_404, redirect

from .models import Capteur
from .forms import RechercheCapteurForm, CapteurForm

def capteur_ajouter(request):
    if request.method == "POST":
        form = CapteurForm(request.POST)
        if form.is_valid():
            capteur = form.save()
            return redirect("capteurs:detail", pk=capteur.pk)
    else:
        form = CapteurForm()

    return render(request, "capteurs/capteur_form.html", {
        "form": form,
        "titre": "Ajouter un capteur",
    })



def capteur_liste(request):
    capteurs = Capteur.objects.order_by("nom")

    if request.GET:
        # Des paramètres sont présents dans l'URL : on lie le formulaire à ces données.
        form = RechercheCapteurForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if q:
                capteurs = capteurs.filter(nom__icontains=q)
            if form.cleaned_data["actifs_seulement"]:
                capteurs = capteurs.filter(actif=True)
        else:
            # Saisie invalide : aucun résultat, le formulaire affichera ses erreurs.
            capteurs = Capteur.objects.none()
    else:
        # Aucune recherche : formulaire vide et liste complète.
        form = RechercheCapteurForm()

    return render(request, "capteurs/capteur_liste.html", {
        "capteurs": capteurs,
        "form": form,
    })


def capteur_detail(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    return render(request, "capteurs/capteur_detail.html", {"capteur": capteur})

def capteur_modifier(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)
    titre = f"Modifier {capteur.nom}"  # calculé avant que le formulaire touche à l'objet

    if request.method == "POST":
        form = CapteurForm(request.POST, instance=capteur)
        if form.is_valid():
            form.save()
            return redirect("capteurs:detail", pk=capteur.pk)
    else:
        form = CapteurForm(instance=capteur)

    return render(request, "capteurs/capteur_form.html", {
        "form": form,
        "titre": titre,
    })

def capteur_supprimer(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)

    if request.method == "POST":
        capteur.delete()
        return redirect("capteurs:liste")

    return render(request, "capteurs/capteur_confirmer_suppression.html", {
        "capteur": capteur,
    })

