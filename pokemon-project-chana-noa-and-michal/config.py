"""
configurate the conect
"""
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

pokemon_url = "https://pokeapi.co/"
flask_port=5000
