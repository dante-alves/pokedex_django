from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Pokemon, PokemonType
from io import BytesIO
from django.core.files.base import ContentFile

import requests
# Create your views here.
def search_pokemon(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        if name:
            return redirect("pokedex:show", name=name)
        
    return render(request, "pokedex/search_pokemon.html")
    
def show_pokemon(request, name):
    # Obter os dados da API do Pokémon
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}/", verify=False)
    
    if response.status_code == 200:
        data = response.json()
        
        # Informações do Pokémon
        pokedex_id = data["id"]
        pokemon_name = data["name"]
        types = [t["type"]["name"] for t in data["types"]]
        sprite_url = data["sprites"]["front_default"]
        
        # Verificar se o Pokémon já existe no banco de dados
        pokemon, created = Pokemon.objects.get_or_create(pokedex_id=pokedex_id, defaults={
            'name': pokemon_name
        })
        
        # Atualizar o nome caso o Pokémon já exista mas tenha outro nome (não esperado, mas é uma boa prática)
        if not created and pokemon.name != pokemon_name:
            pokemon.name = pokemon_name
            pokemon.save()
        
        # Adicionar tipos ao Pokémon
        for type_name in types:
            pokemon_type, _ = PokemonType.objects.get_or_create(name=type_name)
            pokemon.types.add(pokemon_type)
        
        # Baixar a imagem do sprite e salvar
        if sprite_url and not pokemon.sprite:
            response_sprite = requests.get(sprite_url, verify=False)
            if response_sprite.status_code == 200:
                # Criar um arquivo a partir da imagem recebida
                image_data = BytesIO(response_sprite.content)
                pokemon.sprite.save(f"{pokemon_name}.png", ContentFile(image_data.read()), save=True)
        
        # Retornar os dados para o template
        return render(request, "pokedex/show_pokemon.html", {"pokemon": pokemon})
    
    return JsonResponse({"error": "Não foi possível buscar o Pokémon"}, status=500)

def pokemons_by_generation(request, generation_id):

    response = requests.get(f"https://pokeapi.co/api/v2/generation/{generation_id}/", verify=False)

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