from django import forms
from .models import Capteur


class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ["nom", "type_capteur", "emplacement", "actif", "description"]


class RechercheCapteurForm(forms.Form):
    q = forms.CharField(
        label="Nom contient",
        max_length=40,
        required=False,
    )
    actifs_seulement = forms.BooleanField(
        label="Actifs seulement",
        required=False,
    )
