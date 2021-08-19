import json

import requests

from config import pokemon_url
from insertions import insert_query
from queries import get_id_by_name, delete_pokemon_by_id, update_pokemon

from flask import Response

from config import connection

def get_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = f'select name from types,pokemon where types.pokemon_type="{type}" and pokemon_id = id;'
            cursor.execute(query)
            res = cursor.fetchall()
            pokemons_list = []
            for type in res:
                pokemons_list.append(str(type["name"]))
        return (str(pokemons_list),"\nstatus code:200")
    except:
        return ("faild","status code:500")


def get_trainers(pokemon_id):
    try:
        with connection.cursor() as cursor:
            query = f'select owner_name from belonging where pokemon_id ="{pokemon_id}";'
            cursor.execute(query)
            res = cursor.fetchall()
            names_list = []
            for name in res:
                names_list.append(str(name["owner_name"]))
        return (str(names_list), "\nstatus code:200")
    except:
        return ("failed","status code:500")


def get_pokemons(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT  name FROM pokemon,belonging where belonging.owner_name= "{trainer_name}" and pokemon_id=id;'
            cursor.execute(query)
            res = cursor.fetchall()
            names_list = []
            for name in res:
                names_list.append(str(name['name']))
        return (str(names_list),"\nstatus code:200")
    except:
        return ("failed","status code:500")



def add_pokemon(pokemon_params):
    try:
        with connection.cursor() as cursor:
            values_list = ["id", "name", "type", "height", "weight"]
            final_list = []
            for i in values_list:
                if pokemon_params.get(i) == None:
                    pokemon_params[i] = 'null'
                final_list.append(pokemon_params[i])
            query = f'INSERT into pokemon values {tuple(final_list)};'
            cursor.execute(query)
            connection.commit()
            return ("succeeded","status code:200")
    except Exception as exp:
        print(exp)
        return ("failed","status code:500")


def update_types(pokemon_name):
    try:
        pokeUrl = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_name)
        types = requests.get(url=pokeUrl, verify=False)
        dict = json.loads(types.text)
        for item in dict['types']:
            pokemon_id = get_id_by_name(pokemon_name)
            if pokemon_id==None:
                return ("pokemon name not faund",400)
            insert_query('types', [pokemon_id, str(item.get('type')['name'])])
        return ("succeeded",200)
    except:
        return ("failed","status code:500")

def update_types_of_pokemon(pokemon_name):
    poke_url = pokemon_url + "/api/v2/pokemon/{}".format(pokemon_name)
    types = requests.get(url=poke_url, verify=False)
    dict = json.loads(types.text)
    for item in dict['types']:
        pokemon_id = get_id_by_name(pokemon_name)
        if pokemon_id is None:
            return "this pokemon does not exist", str(types.status_code)
        res = insert_query('types', [pokemon_id, str(item.get('type')['name'])])
        return res
    return str(types.status_code)


def delete_pokemon(pokemon_name):
    pokemon_id = get_id_by_name(pokemon_name)
    if pokemon_id is not None:
        res = delete_pokemon_by_id(pokemon_id)
        return res
    else:
        return Response("this pokemon does not exist",400)

def evolve(pokemon_name,trainer_name):
        old_pokemo_id=get_id_by_name(pokemon_name)
        if old_pokemo_id==None:
            return ("pokemon not found",400)
        info_url=f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        try:
            pokemon_general_info=requests.get(url=info_url,verify=False)
            dict = pokemon_general_info.json()
            species_url=dict['species'].get('url')
            pokemon_species=requests.get(url=species_url,verify=False)
            dict=json.loads(pokemon_species.text)
            evolution_chain_url=dict['evolution_chain'].get('url')
            item_chain=requests.get(url=evolution_chain_url,verify=False)
            dict=json.loads(item_chain.text)
            final_name=dict['chain']['evolves_to'][0]['species'].get('name')
            pokemon_id=get_id_by_name(final_name)
            print(final_name)
        except Exception as exp:
            return ("failed","status code:500")
        return update_pokemon(old_pokemo_id,pokemon_id,trainer_name)






