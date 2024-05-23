from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'Usuario con id: {}'.format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
             # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    birht_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"people {self.id} {self.name}"
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "height": self.height,
            "mass": self.mass,
            "birht_year": self.birht_year,
            "gender": self.gender
            }


class Starships(db.Model):
    __tablename__= "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    length = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    consumables = db.Column(db.String(50))

    def __repr__(self):
        return f"starship {self.id} {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "consumables": self.consumables

        }


class Planets(db.Model):
    __tablename__= "planets"
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer,nullable=False)
    orbita_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"planet {self.id} {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbita_period": self.orbita_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
        }

class FavoritePlanets(db.Model):
    __tablename__= "favorite_planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id',))
    user_id_relationship = db.relationship(User)
    planet_id_relationship = db.relationship(Planets)

    def __repr__(self):
        return f"Al usuario {self.user_id} le gusta el planeta {self.planet_id}"
    
    def serialize(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
    
class FavoritePeople(db.Model):
    __tablename__= "favorite_people"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    user_id_relationship = db.relationship(User)
    people_id_relationship = db.relationship(People)

    def __repr__(self):
        return f"Al usuario {self.user_id} le gusta el personaje {self.people_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }

class FavoriteStarships(db.Model):
    __tablename__ = "favorite_starships"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id', ondelete='CASCADE'), nullable=False)
    user_id_relationship = db.relationship(User)
    starship_id_relationship = db.relationship(Starships, backref=db.backref('favorites', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"User {self.user_id} likes starship {self.starship_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }



# class FavoriteStarships(db.Model):
#     __tablename__ = "favorite_starships"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)
#     starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'), nullable=False)
#     user_id_relationship = db.relationship(User)
#     starship_id_relationship = db.relationship(Starships, cascade="all, delete")

#     def __repr__(self):
#         return f"User {self.user_id} likes starship {self.starships_id}"
    
#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "starship_id": self.starship_id
            
#         }

