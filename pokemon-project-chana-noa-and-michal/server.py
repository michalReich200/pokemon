from flask import Flask, request, Response
from config import flask_port
from routing import delete_pokemon, evolve, update_types_of_pokemon, get_trainers, add_pokemon, get_pokemons

app = Flask(__name__, static_url_path='', static_folder="dist")


@app.route('/')
def index():
    return Response("Server is up and running smoothly")


@app.route('/get_by_type/<type>',methods = ['GET'])
def get_by_type(type):
    res = get_by_type(type)
    return Response(res)

@app.route('/get_trainers/<pokemon_id>',methods = ['GET'])
def get__trainers(pokemon_id):
    res = get_trainers(pokemon_id)
    return Response(res)




@app.route('/get_pokemons',methods = ['GET'])
def get_pokemons_by_trainer():
    trainer = request.args
    trainer_name = trainer.get('name')
    res = get_pokemons(trainer_name)
    return Response(res)


@app.route('/add_pokemon', methods=['POST'])
def add_pokemon_to_database():
    pokemon_data = request.args
    res=add_pokemon(pokemon_data)
    return Response(res)

@app.route('/update_types/<pokemon_name>', methods=['GET'])
def update_types(pokemon_name):
    return Response(update_types_of_pokemon(pokemon_name))


@app.route('/delete/<pokemon>', methods=['DELETE'])
def delete_items(pokemon):
    return Response(delete_pokemon(pokemon))


@app.route('/evolve/', methods=['POST'])
def evolve_pokemon():
    trainer = request.args.get('trainer')
    pokemon = request.args.get('pokemon')
    return Response(str(evolve(pokemon, trainer)))


if __name__ == "__main__":
    app.run(port=flask_port)
