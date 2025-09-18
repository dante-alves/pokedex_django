from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

import requests
# Create your views here.
def search_pokemon(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        if name:
            return redirect("pokedex:show", name=name)
        
    return render(request, "pokedex/search_pokemon.html")
    
def show_pokemon(request, name):

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}/")
    
    if response.status_code == 200:
        data = response.json()
        
        pokemon = {
            "pokedex_id" : data["id"],
            "name" : data["name"],
            "types" : [t["type"]["name"] for t in data["types"]],
            "sprite" : data["sprites"]["front_default"],
        }
        
        return render(request, "pokedex/show_pokemon.html", {"pokemon":pokemon})
    
    return JsonResponse({"error": "Não foi possível buscar o Pokémon"}, status=500)

def pokemons_by_generation(request, generation_id):

    response = requests.get(f"https://pokeapi.co/api/v2/generation/{generation_id}/")

    if response.status_code == 200:
        data = response.json()
        pokemons = get_pokemons_with_sprites(data["pokemon_species"])

        paginator = Paginator(pokemons, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "pokedex/pokemons_generation.html", {
            "generation": generation_id,
            "page_obj": page_obj,
        })
    
def get_pokemons_with_sprites(pokemons):
    pokemons_with_sprites = []

    for pokemon in pokemons:

        name = pokemon["name"]

        # pegar o sprite diretamente da url
        url = pokemon["url"].rstrip("/")
        poke_id = url.split("/")[-1]
        sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_id}.png"

        pokemons_with_sprites.append({
            "id": poke_id,
            "name": name,
            "sprite": sprite,
        })
    
    return pokemons_with_sprites