from rest_framework import serializers

from .models import Capteur


class CapteurSerializer(serializers.ModelSerializer):
    type_libelle = serializers.CharField(
        source="get_type_capteur_display",
        read_only=True,
    )

    class Meta:
        model = Capteur
        fields = [
            "id",
            "nom",
            "type_capteur",
            "type_libelle",
            "emplacement",
            "actif",
            "description",
        ]
