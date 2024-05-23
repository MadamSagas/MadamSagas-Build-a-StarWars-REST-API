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
from models import db, User, Planets, People, Starships, FavoritePlanets, FavoritePeople, FavoriteStarships
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
        
    favorite_people = db.session.query(FvoritePeople, People).join(People). \
        filter(FvoritePeople.user_id == id).all()   
    favorite_people_serialized = [] 
    for favorite_person, person in favorite_people:
        favorite_people_serialized.append({'favorite_person_id': favorite_person.id,
                                           "person": person.serialize(),
                                           "user_id": id
                                           })
    favorite_starships= db.session.query(FavotireStarships, Starships).join(Starships).\
        filter(FavotireStarships.user_id == id).all()
    favorite_starships_serialized = []
    for favorite_starship, starship in favorite_starships:
        favorite_starships_serialized.append({
            'favorite_starship_id': favorite_starship.id,
            "starship": starship.serialize(),
            "user_id": id
        })    
    return jsonify({"msg": "OK", "favorite_planets": favorite_planets_serialized, "favorite_people": favorite_people_serialized, 
                    "favorite_starships": favorite_starships_serialized})

@app.route('/favorite/planet/<int:planet_id>', methods=['POST']) 
def add_favorite_planet(planet_id):
    body = request.get_json(silent=True)

    if body is None:  
        return jsonify({"msg": "Debes proporcionar un 'user_id' en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg":"El campo user_id es obligatorio"}), 400

    
    user_id = body['user_id']
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if user is None:
        return jsonify({"msg": f"El usuario con ID {user_id} no existe"}), 404
    
    if planet is None:
        return jsonify({"msg": f"El planeta con el ID {planet_id}, no existe"}), 404
    
    existing_favorite = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"msg": "El paneta ya esta en la lista de Favoritos del Usuario"}), 400
    
    new_fvorite = FavoritePlanets(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fvorite)
    db.session.commit()

    return jsonify({
        "msg": "Nuevo planeta favorito añadido", 
        "data": new_fvorite.serialize()
        }), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_new_favorite_people(people_id):
    body = request.get_json(silent=True)
    
    if body is None:
        return jsonify({"msg": "Debes proporcionar un 'user_id' en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg": "El campo user_id es obligatorio"}), 400

    user_id = body['user_id']
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if user is None:
        return jsonify({"msg": f"El usuario con ID {user_id} no existe"}), 404
    
    if people is None:
        return jsonify({"msg": f"El personaje con ID {people_id} no existe"}), 404
    
    existing_favorites = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    
    if existing_favorites:
        return jsonify({"msg": "El personaje ya está en la lista de favoritos del usuario"}), 400
    
    new_favorite = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({
        "msg": "Nuevo personaje favorito añadido con éxito",
        "data": new_favorite.serialize()
    }), 201


    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes proporcionar un user_id en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg":"El campo user_id es obligatorio"}), 400

    user_id = body['user_id']
    user = User.query.get(user_id)
    starship = Starships.query.get(starships_id)

    if user is None:
        return jsonify({"msg": f"El usuario con el el ID {user_id} no existew"}), 404
    
    if starship is None:
        return jsonify({"msg": f"El starship con el ID {starships_id} no existe"}), 404
    
    existing_favorite = FavoriteStarships.query.filter_by(user_id=user_id, starships_id=starships_id).first()

    if existing_favorite:
        return jsonify({"msg": "El starship ya esta en la lista de favoritos del usuario"}), 400
    
    new_favorite = FavoriteStarships(user_id=user_id, starships_id=starships_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg":"Nuevo starship favorito añadio",
                    "data":new_favorite.serialize()}), 201

@app.route('/favorite/starships/<int:starships_id>', methods=['POST'])
def add_new_favorite_starship(starships_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes proporcionar un user_id en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg": "El campo user_id es obligatorio"}), 400

    user_id = body['user_id']
    user = User.query.get(user_id)
    starship = Starships.query.get(starships_id)

    if user is None:
        return jsonify({"msg": f"El usuario con el ID {user_id} no existe"}), 404
    
    if starship is None:
        return jsonify({"msg": f"El starship con el ID {starships_id} no existe"}), 404
    
    existing_favorite = FavoriteStarships.query.filter_by(user_id=user_id, starships_id=starships_id).first()

    if existing_favorite:
        return jsonify({"msg": "El starship ya está en la lista de favoritos del usuario"}), 400
    
    new_favorite = FavoriteStarships(user_id=user_id, starships_id=starships_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Nuevo starship favorito añadido",
                    "data": new_favorite.serialize()}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes proporcionar un user_id en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg": "El campo user_id es obligatorio"}), 400

    user_id = body['user_id']
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if user is None:
        return jsonify({"msg": f"El planeta con el ID {user_id} no existe"}), 404

    if planet is None:
        return jsonify({"msg":f"el planeta con el ID {planet_id} no existe"}), 

    favorite_planet = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if favorite_planet is None:
        return jsonify({"msg": "El planeta no esta en la lista de favoritos del usuario"}), 404
    
    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({"msg": "El planeta favorito ha sido eliminado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Obtener el cuerpo de la solicitud en formato JSON
    body = request.get_json(silent=True)

    # Validar que el cuerpo de la solicitud no esté vacío
    if body is None:
        return jsonify({"msg": "Debes proporcionar un user_id en el body de la solicitud"}), 400
    if 'user_id' not in body:
        return jsonify({"msg": "El campo user_id es obligatorio"}), 400

    # Extraer user_id del cuerpo de la solicitud
    user_id = body['user_id']

    # Consultar la base de datos para encontrar el usuario y el personaje (people)
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    # Verificar si el usuario existe
    if user is None:
        return jsonify({"msg": f"El usuario con el ID {user_id} no existe"}), 404
    
    # Verificar si el personaje (people) existe
    if people is None:
        return jsonify({"msg": f"El personaje con el ID {people_id} no existe"}), 404

    # Buscar el favorito específico en la base de datos
    favorite_people = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()

    # Verificar si el favorito existe
    if favorite_people is None:
        return jsonify({"msg": "El personaje no está en la lista de favoritos del usuario"}), 404

    # Eliminar el favorito de la base de datos
    db.session.delete(favorite_people)
    db.session.commit()

    # Responder con un mensaje de éxito
    return jsonify({"msg": "El personaje favorito ha sido eliminado"}), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes proporcionar un user_id en el body de la solicitud"}), 400
    
    if 'user_id' not in body:
        return jsonify({"msg":"El campo user_id es obligatorio"}), 400

    user_id = body['user_id']
    user = User.query.get(user_id)
    starship = Starships.query.get(starship_id)

    if user is None:
        return jsonify({"msg": f"El usuario con el ID {user_id} no existe"}), 404
    if starship is None:
        return jsonify({"msg":f"El starship con el ID {starship_id} no existe"}), 404

    favorite_starship = FavoriteStarships.query.filter_by(user_id=user_id, starships_id=starship_id).first()

    if favorite_starship is None:
        return jsonify({"msg": "El starship no esta en la lista de favoritos del usuario"}), 404
    
    db.session.delete(favorite_starship)
    db.session.commit()

    return jsonify({"msg":"El starship favorito ha sido eliminado"}), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"msg": f"El planeta con el ID {planet_id}, no existe"}), 404
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": "El planeta ha sido eliminado"}), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    # Buscar el registro en la base de datos
    people = People.query.get(people_id)

    if people is None:
        return jsonify({"msg": f"El personaje con el ID {people_id} no existe"}), 404

    # Eliminar el registro de la base de datos
    favorite_people = FavoritePeople.query.filter_by(people_id=people_id,).all()
    for favorite in favorite_people:
        db.session.delete(favorite)

    db.session.delete(people)
    db.session.commit()

    return jsonify({"msg": "El personaje ha sido eliminado"}), 200

@app.route('/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    starship = Starships.query.get(starship_id)

    if starship is None:
        return jsonify({"msg":f"El starship con el ID{starship_id}, no existe"}), 404
    
    # favorite_starship = FavoriteStarships.query.filter_by(starship_id=starship_id).all()
    # for favorite in favorite_starship:
    #     db.session.delete(favorite)

    db.session.delete(starship)
    db.session.commit()

    return jsonify({"msg":"El starship ha sido eliminado"}), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg":"Debes enviar informacion en el body"}), 400
    
    # Consultar la base de datos para encontrar el planeta por su ID
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": f"El planeta con el ID {planet_id}, no exite"}), 404
    
    # Actualizar los campos si están presentes en el body
    if "name" in body:
        planet.name = body["name"]
    if "population" in body:
        planet.population = body["population"]
    if "rotation_period" in body:
        planet.rotation_period = body["rotation_period"]
    if "orbita_period" in body:
        planet.orbita_period = body["orbita_period"]
    if "diameter" in body:
        planet.diameter = body["diameter"]
    if "climate" in body:
        planet.climate = body["climate"]
    if "terrain" in body:
        planet.terrain = body["terrain"]

    db.session.commit()

    return jsonify({"msg": "El planeta ha sido alctualizado",
                    "data": planet.serialize()}), 200

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes enviar informacion el el body"}), 400
    
    people = People.query.get(people_id)

    if people is None:
        return jsonify({"msg":f"El personaje con el ID {people_id}, no existe"}), 404
    
    if "name" in body:
        people.name = body["name"]
    if "last_name" in body:
        people.last_name = body["last_name"]
    if "height" in body:
        people.height = body["height"]
    if "mass" in body:
        people.mass = body["mass"]
    if "birht_year" in body:
        people.birht_year = body["birht_year"]
    if "gender" in body:
        people.gender = body["gender"]

    db.session.commit()

    return jsonify({"msg": "El personaje ha sido actualizado",
                    "data": people.serialize()}), 200

@app.route('/starship/<int:starship_id>', methods=['PUT'])
def update_starship(starship_id):
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"msg": "Debes enviar informacion en el boody"}), 400
    
    starship = Starships.query.get(starship_id)
    if starship is None:
        return jsonify({"msg": F"El starship con el ID {starship_id} no existe"}), 404
    
    if "name" in body:
        starship.name = body["name"]
    if "model" in body:
        starship.model = body["model"]
    if "manufacturer" in body:
        starship.manufacturer = body["manufacturer"]
    if "length" in body:
        starship.length = body["length"]
    if "crew" in body:
        starship.crew = body["crew"]
    if "passengers" in body:
        starship.passengers = body["passengers"]

    db.session.commit()

    return jsonify({"msg": "EL starship ha sido actualizado",
                    "data": starship.serialize()}), 200
    



    


# Updating data

# user1 = Person.query.get(person_id) <- sirve solo para PK
# if user1 is None:
#     return jsonify({'msg':'User not found'},404

# if "username" in body:
#     user1.username = body["username"]
# if "email" in body:
#     user1.email = body["email"]
# db.session.commit()

# user1 = Person.query.get(person_id)
# if user1 is None:
#    return jsonify({'msg':'User not found'},404
# db.session.delete(user1)
# db.session.commit()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
