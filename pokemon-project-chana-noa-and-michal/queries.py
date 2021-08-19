"""
implement functions on the pokemons.
"""

from config import connection


def heaviest_pokemon():
    with connection.cursor() as cursor:
        try:
            query = 'SELECT max(height) FROM pokemon ;'
            cursor.execute(query)
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if res is None:
            return None
        return res


def find_name_by_type(type):
    with connection.cursor() as cursor:
        try:
            query = f'select name from pokemon where pokemon.type="{type}";'
            cursor.execute(query)
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if res is None:
            return None
        names_list = []
        for elem in res:
            names_list.append(elem['name'])
        return names_list


def find_owners(pokemon_name):
    with connection.cursor() as cursor:
        try:
            query = f'select owner_name from pokemon,belonging where pokemon.id=belonging.pokemon_id and pokemon.name="{pokemon_name}"; '
            cursor.execute(query)
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if res is None:
            return None
        names_list = []
        for elem in res:
            names_list.append(elem['owner_name'])
        return names_list


def finds_most_owned():
    with connection.cursor() as cursor:
        try:
            query = f'select name from pokemon where pokemon.id in(SELECT id FROM (select pokemon_id as id ,max(count) from ' \
                    f'(select pokemon_id, count(*) as count from belonging group by pokemon_id) as owners_g)as ids); '
            cursor.execute(query)
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if res is None:
            return None
        names_list = []
        for elem in res:
            names_list.append(elem['name'])
        return names_list


def get_pokemons_by_trainer(trainer_name):
    with connection.cursor() as cursor:
        try:
            query = f'SELECT distinct name  FROM pokemon,belonging where belonging.owner_name= "{trainer_name}" and ' \
                    f'pokemon_id=id; '
            cursor.execute(query)
            connection.commit()
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if not res:
            return None
        names_list = []
        for elem in res:
            names_list.append(elem['name'])
        return names_list


def get_id_by_name(name):
    with connection.cursor() as cursor:
        try:
            query = f'select id from pokemon where name="{name}";'
            cursor.execute(query)
        except connection.Error as err:
            return "Something went wrong: {}".format(err)
        res = cursor.fetchall()
        if not res:
            return None
        return res[0].get('id')


def delete_pokemon_by_id(pokemon_id):
    with connection.cursor() as cursor:
        try:
            query = f'delete from pokemon where id="{pokemon_id}";'
            cursor.execute(query)
            connection.commit()

        except:

            return (f'could not found {pokemon_id} in pokemon table', 400)

        try:
            new_query = f'delete from belonging where pokemon_id="{pokemon_id}";'
            cursor.execute(new_query)
            connection.commit()

        except:
            return (f'could not found {pokemon_id} in belonging table',400)

        try:
            query3 = f'delete from types where pokemon_id="{pokemon_id}";'
            cursor.execute(query3)
            connection.commit()
        except:
            return (f'could not found {pokemon_id} in types table',400)

        return ("succeeded",200)




def update_pokemon(pokemon_id, new_pokemon_id, trainer_name):
    with connection.cursor() as cursor:
        try:
            query = f'update belonging set pokemon_id="{new_pokemon_id}" where owner_name="{trainer_name}" and pokemon_id="{pokemon_id}"'
            cursor.execute(query)
            connection.commit()
        except:
            return ("could not found one of the following:trainer name or pokemon name",400)
        return ("succeeded", 200)


