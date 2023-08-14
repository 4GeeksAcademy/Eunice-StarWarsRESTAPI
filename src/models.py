from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), index=True, unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(15), index=True, unique=True, nullable=False)
    url = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Characters %r>" % self.username

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(15), index=True, unique=True, nullable=False)
    url = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Planets %r>" % self.username

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(15), index=True, unique=True, nullable=False)
    url = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return "<Vehicles %r>" % self.username

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "url": self.url
        }


class CharacterDetails(db.Model):
    __tablename__ = "characters_details"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey(
        "characters.uid"), unique=True, nullable=False)
    gender = db.Column(db.String(15))
    height = db.Column(db.String(15))
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(15))
    eye_color = db.Column(db.String(15))
    hair_color = db.Column(db.String(15))
    birth_year = db.Column(db.String(15))
    planetland = db.Column(db.Integer, db.ForeignKey("planets.id"))
    characters = db.relationship(Characters)
    planets = db.relationship(Planets)

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "gender": self.gender,
            "height": self.heigt,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "planetland": self.planetland
        }


class PlanetDetails(db.Model):
    __tablename__ = "planets_details"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey(
        "planets.uid"), unique=True, nullable=False)
    population = db.Column(db.String)
    gravity = db.Column(db.Float)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    climate = db.Column(db.String(15))
    terrain = db.Column(db.String(15))
    surface_water = db.Column(db.String(15))
    planets = db.relationship(Planets)

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "population": self.population,
            "gravity": self.gravity,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }


class VehicleDetails(db.Model):
    __tablename__ = "vehicles_details"
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey(
        "vehicles.uid"), unique=True, nullable=False)
    model = db.Column(db.String(15))
    vehicle_class = db.Column(db.String(15))
    manufacturer = db.Column(db.String(15))
    cost_in_credits = db.Column(db.Integer)
    length = db.Column(db.Float)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    max_atmosphering_speed = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)
    consumables = db.Column(db.String(15))
    vehicles = db.relationship(Vehicles)

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    user = db.relationship(User)
    characters = db.relationship(Characters)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }


class FavoriteVehicle(db.Model):
    __tablename__ = "favorite_vehicles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    user = db.relationship(User)
    vehicles = db.relationship(Vehicles)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    user = db.relationship(User)
    planets = db.relationship(Planets)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
