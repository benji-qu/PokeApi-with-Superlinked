import requests as req
import pandas as pd

POKEAPI = 'http://pokeapi.co/api/v2'
endpoints = req.get(POKEAPI).json()

pokemon_general_info = req.get(f"{endpoints['pokemon']}?offset=0&limit={1200}").json()['results']
pokemon_species_info = req.get(f"{endpoints['pokemon-species']}?offset=0&limit={1200}").json()['results']

n = min(len(pokemon_general_info), len(pokemon_species_info))

def get_data(id):
    pokemon_g = pokemon_general_info[id-1]
    pokemon_s = pokemon_species_info[id-1]

    data = req.get(pokemon_g['url']).json()
    species = req.get(pokemon_s['url']).json()
    name = pokemon_g['name']
    abilities = [i['ability']['name'] for i in data['abilities']]
    height = data['height']
    weight = data['weight']
    poke_type = data['types'][0]['type']['name']
    sprite = data['sprites']['front_default']
    color = species['color']['name']
    capture_chance = round(species['capture_rate']/255,2)
    # not every pokemon entry has shape and habitat filled in, so we have to check this field
    try: 
        shape = species['shape']['name']
    except:
        shape = None
    try:
        habitat = species['habitat']['name']
    except:
        habitat = None

    res = {'id': id, 'name': name, 'abilities': abilities, 
            'color': color, 'shape' : shape, 'habitat': habitat, 'capture_chance': capture_chance,
            'height': height,'weight': weight, 'poke_type': poke_type,
            'sprite': sprite}
    return res


pokedex_list = [get_data(i) for i in range(1, n+1)]
pokedex_df = pd.DataFrame(pokedex_list)
pokedex_df.to_csv('data/pokedex_temp.csv')