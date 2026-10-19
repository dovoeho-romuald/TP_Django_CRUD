from django.test import Client, TestCase
from django.urls import reverse

from .models import Capteur


class ProtectionCsrfTests(TestCase):
    """Scénario 11 : un POST sans jeton CSRF est refusé (403) et ne modifie rien."""

    def setUp(self):
        self.capteur = Capteur.objects.create(
            nom="Temp-Serre", type_capteur="T", emplacement="Serre A",
        )
        # Par défaut, le client de test ne vérifie PAS le CSRF : on l'active.
        self.client = Client(enforce_csrf_checks=True)

    def test_ajouter_sans_csrf_refuse(self):
        reponse = self.client.post(reverse("capteurs:ajouter"), {
            "nom": "Pirate", "type_capteur": "T", "emplacement": "Ailleurs",
        })
        self.assertEqual(reponse.status_code, 403)
        self.assertEqual(Capteur.objects.count(), 1)

    def test_modifier_sans_csrf_refuse(self):
        url = reverse("capteurs:modifier", args=[self.capteur.pk])
        reponse = self.client.post(url, {
            "nom": "Pirate", "type_capteur": "T", "emplacement": "Ailleurs",
        })
        self.assertEqual(reponse.status_code, 403)
        self.capteur.refresh_from_db()
        self.assertEqual(self.capteur.nom, "Temp-Serre")

    def test_supprimer_sans_csrf_refuse(self):
        url = reverse("capteurs:supprimer", args=[self.capteur.pk])
        reponse = self.client.post(url)
        self.assertEqual(reponse.status_code, 403)
        self.assertTrue(Capteur.objects.filter(pk=self.capteur.pk).exists())


class ListeVideTests(TestCase):
    """Scénario 12 : base de test vide, message clair et lien Ajouter présent."""

    def test_liste_vide(self):
        reponse = self.client.get(reverse("capteurs:liste"))
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Aucun capteur")
        self.assertContains(reponse, reverse("capteurs:ajouter"))
