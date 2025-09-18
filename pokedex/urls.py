from django.urls import path
from .views import show_pokemon, search_pokemon, pokemons_by_generation
from django.conf import settings
from django.conf.urls.static import static

app_name = "pokedex"

urlpatterns = [
    path('generation/<int:generation_id>/', pokemons_by_generation, name='generation'),
    path('search/', search_pokemon, name='search'),
    path('show/<str:name>/', show_pokemon, name='show'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
