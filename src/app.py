"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Starships, FavoritePlanets
#traer todas las tables creados

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    # variable donde se guardan los users que tre el query all_users
    # print(all_users[0].serialize())
    # print('tipo de dato': type(all_users[0].serialize()))
    all_users = User.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({"data": users_serialized}), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    single_user = User.query.get(id)
    if single_user is None:
        return jsonify({"msg": "El usuario con el ID : {} NO EXISTE".format(id)}), 400
    return jsonify({"data": single_user.serialize()}), 200
    # user1 = Person.query.get(person_id)

@app.route('/people', methods=['GET'])
def get_people():
    #people_query = Person.query.all()
    all_people = People.query.all()
    people_serialized = []
    for peop in all_people:
        people_serialized.append(peop.serialize())
    print(people_serialized)
    return jsonify({"data": people_serialized}), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_single_people(id):
    single_people = People.query.get(id)
    if single_people is None:
        return jsonify({"msg": "El usuario con el ID : {} NO EXISTE".format(id)})
    return jsonify({"data": single_people.serialize()}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    planets_serialized = []
    for planet in all_planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)
    return jsonify({"data": planets_serialized})

@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet is None:
        return jsonify({"msg": "El planeta con el ID: {} NO EXISTE".format(id)})
    return jsonify({"data": single_planet.serialize()}), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    all_starships = Starships.query.all()
    starships_serialized = []
    for starship in all_starships:
        starships_serialized.append(starship.serialize())
    print(starships_serialized)
    return jsonify({"data": starships_serialized})

@app.route('/starships/<int:id>', methods=['GET'])
def get_single_starship(id):
    single_starship = Starships.query.get(id)
    if single_starship is None:
        return jsonify({"msg": "El Starship con el ID: {} NO EXISTE".format(id)})
    return jsonify({"data": single_starship.serialize()}), 200


@app.route("/planet", methods=['POST'])
def new_planet():

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatirio"}), 400
    if "population" not in body:
        return jsonify({"msg": "El campo population es obligatirio"}), 400
    if "rotation_period" not in body:
        return jsonify({"msg": "El campo rotation_period es obligatirio"}), 400
    if "orbita_period" not in body:
        return jsonify({"msg": "El campo orbita_period es obligarorio"}), 400
    if "diameter" not in body:
        return jsonify({"msg": "El campo diameter es obligatirio"}), 400
    if "climate" not in body:
        return jsonify({"msg": "El campo climate es obligatirio"}), 400
    if "terrain"  not in body:
        return jsonify({"msg": "El campo terrain es obligatirio"}), 400
    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body["population"]
    new_planet.rotation_period = body["rotation_period"]
    new_planet.orbita_period = body["orbita_period"]
    new_planet.diameter = body["diameter"]
    new_planet.climate = body["climate"]
    new_planet.terrain = body["terrain"]
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg": "Nuevo planeta creado",
                    "data": new_planet.serialize()}), 201



    '''
    user1 = Person()
    user1.username = "my_super_username"
    user1.email = "my_super@email.com"
    db.session.add(user1)
    db.session.commit()
    '''
    
@app.route("/people", methods=['POST'])
def new_people():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar informacion de el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatirio"}), 400
    if "height" not in body:
        return jsonify({"msg": "El campo height es obligatorio"}), 400
    if "mass" not in body:
        return jsonify({"msg": "El campo mass es obligatorio"}), 400
    if "birht_year" not in body:
        return jsonify({"msg": "El campo birht_year es obligatorio"}), 400
    if "gender" not in body:
        return jsonify({"msg": "El campo gender es obligatorio"}), 400
    new_people = People()
    new_people.name = body["name"]
    new_people.last_name = body["last_name"]
    new_people.height = body["height"]
    new_people.mass = body["mass"]
    new_people.birht_year = body["birht_year"]
    new_people.gender = body["gender"]
    db.session.add(new_people)
    db.session.commit()
    return jsonify({"msg":"New People created",  
                    "data": new_people.serialize()}), 201

@app.route("/starships", methods=['POST'])
def new_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar información en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatorio"}), 400
    if "population" not in body:
        return jsonify({"msg": "El campo population es obligatorio"}), 400
    if "rotation_period" not in body:
        return jsonify({"msg": "El campo rotation_period es obligatorio"}), 400
    if "orbita_period" not in body:
        return jsonify({"msg": "El campo orbita_period es obligatorio"}), 400
    if  "diameter" not in body:
        return jsonify({"msg":"El campo diameter es obligatorio"}), 400
    if "climate" not in body:
        return jsonify({"msg": "El campo climate es obligatorio"}), 400
    if "terrain" not in body:
        return jsonify({"msg": "El terrain climate es obligatorio" }), 400
    new_starship = Starships()
    new_starship.name = body["name"]
    new_starship.population= body["population"]
    new_starship.rotation_period = body["rotation_period"]
    new_starship.orbita_period = body["orbita_period"]
    new_starship.diameter = body["diameter"]
    new_starship.climate = body["climate"]
    new_starship.terrain = body["terrain"]
    db.session.add(new_starship)
    db.session.commit()
    return jsonify({"msg": "New Starship created",
                    "data": new_starship.serialize()}), 201

@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"msg": f"El usuariio con ID {id} existe"}), 404
    favorite_planets = db.session.query(FavoritePlanets, Planets).join(Planets).\
        filter(FavoritePlanets.user_id == id).all()
    favorite_planets_serialized = []
    for favorite_planet, planet in favorite_planets:
        favorite_planets_serialized.append({'favorite_planet_id': favorite_planet.id, 
                                            "planet": planet.serialize(), 
                                            "user_id": id})
    return jsonify({"msg": "OK", "data": favorite_planets_serialized})

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
