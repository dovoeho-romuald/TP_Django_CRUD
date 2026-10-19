from django.contrib import admin
from django.urls import include, path

from capteurs import views as capteurs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('capteurs/', include('capteurs.urls')),

    # API (GET seulement)
    path('api/capteurs/', capteurs_views.api_capteur_liste, name='api_capteur_liste'),
    path('api/capteurs/<int:pk>/', capteurs_views.api_capteur_detail, name='api_capteur_detail'),
    path('api/capteurs/temperature/', capteurs_views.api_capteurs_par_type, {'code': 'T'}, name='api_capteurs_temperature'),
    path('api/capteurs/humidite/', capteurs_views.api_capteurs_par_type, {'code': 'H'}, name='api_capteurs_humidite'),
    path('api/capteurs/pression/', capteurs_views.api_capteurs_par_type, {'code': 'P'}, name='api_capteurs_pression'),
]
