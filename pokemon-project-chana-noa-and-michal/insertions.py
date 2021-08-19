"""
insert the pokemons data to database
"""

import pymysql
from config import connection
import json


def insert_data():
    with open("pokemon_data.json", 'r') as data:
        data_dict = json.load(data)
        values_list = ["id", "name", "type", "height", "weight"]
        final_list = []
        owners=[]
        for element in data_dict:
            for i in values_list:
                if element.get(i) == None:
                    element[i] = 'null'
                final_list.append(element[i])
            # insert_query("pokemon", final_list)
            for owner in element['ownedBy']:
                if owner not in owners:
                    owners.append(owner)
                    # insert_query('owners', [owner['name'], owner['town']])
                insert_query('belonging', [owner['name'], owner['town'], final_list[0]])
            final_list = []
        return "done"


def insert_query(table, values=[]):
    with connection.cursor() as cursor:
        try:
            values_tuple = tuple(values)
            query = f'INSERT into {table} values{values_tuple};'
            cursor.execute(query)
            connection.commit()
        except connection.Error as err:
            return err
        return "done"


