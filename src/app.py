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
from models import db, User, Characters, Planets, Vehicles, Characters_Details, Planets_Details, Vehicles_Details, Favorite_Characters, Favorite_Planets, Favorite_Vehicles
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route("/")
def sitemap():
    return generate_sitemap(app)

# <-- User Methods -->


@app.route("/user", methods=["GET"])
def handle_hello():
    users = User.query.all()
    if not users:
        raise APIException(
            f"No users", status_code=400)
    all_user = list(map(lambda user: user.serialize(), users))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": all_user
    }

    return jsonify(response_body), 200


@app.route("/user", methods=["POST"])
def post_user():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "username" not in request_body:
        raise APIException("Username is required", status_code=400)
    if "email" not in request_body:
        raise APIException("Email is required", status_code=400)
    if "password" not in request_body:
        raise APIException("Password is required", status_code=400)

    user = User(username=request_body["username"],
                email=request_body["email"], password=request_body["password"])
    user.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/user/<int:user_id>", methods=["PUT"])
def put_user(user_id):
    request_body = request.get_json(force=True)
    user = User.query.get(user_id)
    if request_body is None:
        raise APIException("You must send new information", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "username" in request_body:
        user.username = request_body["username"]
    if "email" in request_body:
        user.email = request_body["email"]
    if "password" in request_body:
        user.password = request_body["password"]

    user.update()
    return jsonify({"msg": "Updated"}), 200


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("The user doesn't exist", status_code=400)

    user.delete()
    return jsonify({"msg": "Completed"}), 200

# <-- Characters Methods -->


@app.route("/characters", methods=["GET"])
def get_characters():
    characters = Characters.query.all()

    if not characters:
        response_body = {
            "msg": "No characters available."
        }
    else:
        all_characters = list(
            map(lambda characters: characters.serialize(), characters))
        response_body = {
            "msg": "GET /characters response",
            "characters": all_characters
        }

    return jsonify(response_body), 200


@app.route("/characters", methods=["POST"])
def post_character():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is required", status_code=400)
    if "name" not in request_body:
        raise APIException("Name is required", status_code=400)
    if "url" not in request_body:
        raise APIException("Url is required", status_code=400)

    character = Characters(
        uid=request_body["uid"], name=request_body["name"], url=request_body["url"])
    character.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/characters/<int:character_uid>", methods=["PUT"])
def put_character(character_uid):
    request_body = request.get_json(silent=True)

    character = Characters.query.filter_by(uid=character_uid).first()

    if character is None:
        raise APIException("Character not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        character.uid = request_body["uid"]
    if "name" in request_body:
        character.name = request_body["name"]
    if "url" in request_body:
        character.url = request_body["url"]

    character.update()

    return jsonify({"msg": "Updated"}), 200


@app.route("/characters/<int:character_uid>", methods=["DELETE"])
def delete_character(character_uid):
    character = Characters.query.filter_by(uid=character_uid).first()

    if character is None:
        raise APIException("Character not found", status_code=400)

    character.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Characters Details -->


@app.route("/characters/details/<int:character_uid>", methods=["GET"])
def get_characters_details(character_uid):
    characters_details = Characters_Details.query.filter_by(
        uid=character_uid).first()

    if not characters_details:
        response_body = {
            "msg": "No character details available."
        }
        return jsonify(response_body), 404
    else:
        response_body = {
            "msg": "ok",
            "characters_details": characters_details.serialize()
        }
        return jsonify(response_body), 200


@app.route("/characters/details", methods=["POST"])
def post_character_details():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is required", status_code=400)
    if "height" not in request_body:
        raise APIException("Height is required", status_code=400)
    if "mass" not in request_body:
        raise APIException("Mass is required", status_code=400)
    if "hair_color" not in request_body:
        raise APIException("Hair color is required", status_code=400)
    if "skin_color" not in request_body:
        raise APIException("Skin color is required", status_code=400)
    if "eye_color" not in request_body:
        raise APIException("Eye color is required", status_code=400)
    if "birth_year" not in request_body:
        raise APIException("Birth year is required", status_code=400)
    if "gender" not in request_body:
        raise APIException("Gender is required", status_code=400)
    if "planetland" not in request_body:
        raise APIException("Planetland is required", status_code=400)

    character_details = Characters_Details(
        uid=request_body["uid"],
        height=request_body["height"],
        mass=request_body["mass"],
        hair_color=request_body["hair_color"],
        skin_color=request_body["skin_color"],
        eye_color=request_body["eye_color"],
        birth_year=request_body["birth_year"],
        gender=request_body["gender"],
        planetland=request_body["planetland"]
    )

    character_details.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/characters/details/<int:character_uid>", methods=["PUT"])
def put_character_details(character_uid):
    request_body = request.get_json(silent=True)

    characters_details = Characters_Details.query.filter_by(
        uid=character_uid).first()

    if characters_details is None:
        raise APIException("Character Details not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        characters_details.uid = request_body["uid"]
    if "height" in request_body:
        characters_details.height = request_body["height"]
    if "mass" in request_body:
        characters_details.mass = request_body["mass"]
    if "hair_color" in request_body:
        characters_details.hair_color = request_body["hair_color"]
    if "skin_color" in request_body:
        characters_details.skin_color = request_body["skin_color"]
    if "eye_color" in request_body:
        characters_details.eye_color = request_body["eye_color"]
    if "birth_year" in request_body:
        characters_details.birth_year = request_body["birth_year"]
    if "gender" in request_body:
        characters_details.gender = request_body["gender"]
    if "planetland" in request_body:
        characters_details.planetland = request_body["planetland"]

    characters_details.update()

    return jsonify({"msg": "Updated"}), 200


@app.route("/characters/details/<int:character_uid>", methods=["DELETE"])
def delete_character_details(character_uid):
    character_details = Characters_Details.query.filter_by(
        uid=character_uid).first()

    if character_details is None:
        raise APIException("Character Details not found", status_code=400)

    character_details.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Planets Methods -->


@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()

    if not planets:
        response_body = {
            "msg": "No planets available"
        }
    else:
        all_planets = list(map(lambda planets: planets.serialize(), planets))
        response_body = {
            "msg": "GET/ planets response",
            "planets": all_planets
        }
    return jsonify(response_body), 200


@app.route("/planets", methods=["POST"])
def post_planets():
    request_body = request.get_json(silent=True)

    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is requerid", status_code=400)
    if "name" not in request_body:
        raise APIException("Name is requerid", status_code=400)
    if "url" not in request_body:
        raise APIException("Url is requerid", status_code=400)

    planets = Planets(
        uid=request_body["uid"], name=request_body["name"], url=request_body["url"])
    planets.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/planets/<int:planet_uid>", methods=["PUT"])
def put_planet(planet_uid):
    request_body = request.get_json(silent=True)
    planet = Planets.query.filter_by(uid=planet_uid).first()

    if planet is None:
        raise APIException("Planet not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        planet.uid = request_body["uid"]
    if "name" in request_body:
        planet.name = request_body["name"]
    if "url" in request_body:
        planet.url = request_body["url"]

    planet.update()

    return jsonify({"msg": "Completed"}), 200


@app.route("/planets/<int:planet_uid>", methods=["DELETE"])
def delete_planet(planet_uid):
    planet = Planets.query.filter_by(uid=planet_uid).first()

    if planet is None:
        raise APIException("Character not found", status_code=400)

    for detail in planet.characters_details:
        detail.planetland = None

    planet.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Planets Details -->

@app.route("/planets/details/<int:planet_uid>", methods=["GET"])
def get_planets_details(planet_uid):
    planets_details = Planets_Details.query.filter_by(
        uid=planet_uid).first()

    if not planets_details:
        response_body = {
            "msg": "No planet details available."
        }
        return jsonify(response_body), 404
    else:
        response_body = {
            "msg": "ok",
            "planets_details": planets_details.serialize()
        }
        return jsonify(response_body), 200


@app.route("/planets/details", methods=["POST"])
def post_planet_details():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is required", status_code=400)
    if "population" not in request_body:
        raise APIException("Population is required", status_code=400)
    if "gravity" not in request_body:
        raise APIException("Gravity is required", status_code=400)
    if "rotation_period" not in request_body:
        raise APIException("Rotation period is required", status_code=400)
    if "orbital_period" not in request_body:
        raise APIException("Orbital period is required", status_code=400)
    if "climate" not in request_body:
        raise APIException("Climate is required", status_code=400)
    if "terrain" not in request_body:
        raise APIException("Terrain is required", status_code=400)
    if "surface_water" not in request_body:
        raise APIException("Surface water is required", status_code=400)

    planet_details = Planets_Details(
        uid=request_body["uid"],
        population=request_body["population"],
        gravity=request_body["gravity"],
        rotation_period=request_body["rotation_period"],
        orbital_period=request_body["orbital_period"],
        climate=request_body["climate"],
        terrain=request_body["terrain"],
        surface_water=request_body["surface_water"]
    )

    planet_details.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/planets/details/<int:planet_uid>", methods=["PUT"])
def put_planet_details(planet_uid):
    request_body = request.get_json(silent=True)

    planets_details = Planets_Details.query.filter_by(
        uid=planet_uid).first()

    if planets_details is None:
        raise APIException("planet Details not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        planets_details.uid = request_body["uid"]
    if "population" in request_body:
        planets_details.population = request_body["height"]
    if "gravity" in request_body:
        planets_details.gravity = request_body["gravity"]
    if "rotation_period" in request_body:
        planets_details.rotation_period = request_body["rotation_period"]
    if "orbital_period" in request_body:
        planets_details.orbital_period = request_body["orbital_period"]
    if "climate" in request_body:
        planets_details.climate = request_body["climate"]
    if "terrain" in request_body:
        planets_details.terrain = request_body["terrain"]
    if "surface_water" in request_body:
        planets_details.surface_water = request_body["surface_water"]

    planets_details.update()

    return jsonify({"msg": "Updated"}), 200


@app.route("/planets/details/<int:planet_uid>", methods=["DELETE"])
def delete_planet_details(planet_uid):
    planet_details = Planets_Details.query.filter_by(
        uid=planet_uid).first()

    if planet_details is None:
        raise APIException("Planet Details not found", status_code=400)

    planet_details.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Vehicles Methods -->

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehicles = Vehicles.query.all()

    if not vehicles:
        response_body = {
            "msg": "No vehicles available"
        }
    else:
        all_vehicles = list(
            map(lambda vehicles: vehicles.serialize(), vehicles))
        response_body = {
            "msg": "GET/ vehicles response",
            "vehicles": all_vehicles
        }
    return jsonify(response_body), 200


@app.route("/vehicles", methods=["POST"])
def post_vehicles():
    request_body = request.get_json(silent=True)

    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is requerid", status_code=400)
    if "name" not in request_body:
        raise APIException("Name is requerid", status_code=400)
    if "url" not in request_body:
        raise APIException("Url is requerid", status_code=400)

    vehicles = Vehicles(
        uid=request_body["uid"], name=request_body["name"], url=request_body["url"])
    vehicles.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/vehicles/<int:vehicle_uid>", methods=["PUT"])
def put_vehicle(vehicle_uid):
    request_body = request.get_json(silent=True)
    vehicle = Vehicles.query.filter_by(uid=vehicle_uid).first()

    if vehicle is None:
        raise APIException("vehicle not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        vehicle.uid = request_body["uid"]
    if "name" in request_body:
        vehicle.name = request_body["name"]
    if "url" in request_body:
        vehicle.url = request_body["url"]

    vehicle.update()

    return jsonify({"msg": "Completed"}), 200


@app.route("/vehicles/<int:vehicle_uid>", methods=["DELETE"])
def delete_vehicle(vehicle_uid):
    vehicle = Vehicles.query.filter_by(uid=vehicle_uid).first()

    if vehicle is None:
        raise APIException("Character not found", status_code=400)

    vehicle.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Vehicles Details -->

@app.route("/vehicles/details/<int:vehicle_uid>", methods=["GET"])
def get_vehicles_details(vehicle_uid):
    vehicles_details = Vehicles_Details.query.filter_by(
        uid=vehicle_uid).first()

    if not vehicles_details:
        response_body = {
            "msg": "No vehicle details available."
        }
        return jsonify(response_body), 404
    else:
        response_body = {
            "msg": "ok",
            "vehicles_details": vehicles_details.serialize()
        }
        return jsonify(response_body), 200


@app.route("/vehicles/details", methods=["POST"])
def post_vehicle_details():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is required", status_code=400)
    if "model" not in request_body:
        raise APIException("Model is required", status_code=400)
    if "vehicle_class" not in request_body:
        raise APIException("Vehicle class is required", status_code=400)
    if "manufacturer" not in request_body:
        raise APIException("Manufacturer is required", status_code=400)
    if "cost_in_credits" not in request_body:
        raise APIException("Cost in credits is required", status_code=400)
    if "length" not in request_body:
        raise APIException("Length is required", status_code=400)
    if "crew" not in request_body:
        raise APIException("Crew is required", status_code=400)
    if "passengers" not in request_body:
        raise APIException("Passengers is required", status_code=400)
    if "max_atmosphering_speed" not in request_body:
        raise APIException(
            "Max atmosphering speed is required", status_code=400)
    if "cargo_capacity" not in request_body:
        raise APIException("Cargo capacity is required", status_code=400)
    if "consumables" not in request_body:
        raise APIException("Consumables is required", status_code=400)

    vehicle_details = Vehicles_Details(
        uid=request_body["uid"],
        model=request_body["model"],
        vehicle_class=request_body["vehicle_class"],
        manufacturer=request_body["manufacturer"],
        cost_in_credits=request_body["cost_in_credits"],
        length=request_body["length"],
        crew=request_body["crew"],
        passengers=request_body["passengers"],
        max_atmosphering_speed=request_body["max_atmosphering_speed"],
        cargo_capacity=request_body["crew"],
        consumables=request_body["consumables"]
    )

    vehicle_details.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/vehicles/details/<int:vehicle_uid>", methods=["PUT"])
def put_vehicle_details(vehicle_uid):
    request_body = request.get_json(silent=True)

    vehicles_details = Vehicles_Details.query.filter_by(
        uid=vehicle_uid).first()

    if vehicles_details is None:
        raise APIException("vehicle Details not found", status_code=400)
    if request_body is None or not any(request_body.values()):
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        vehicles_details.uid = request_body["uid"]
    if "model" in request_body:
        vehicles_details.model = request_body["model"]
    if "vehicles_details_class" in request_body:
        vehicles_details.vehicle_class = request_body["vehicle_class"]
    if "manufacturer" in request_body:
        vehicles_details.manufacturer = request_body["manufacturer"]
    if "cost_in_credits" in request_body:
        vehicles_details.cost_in_credits = request_body["cost_in_credits"]
    if "length" in request_body:
        vehicles_details.length = request_body["length"]
    if "crew" in request_body:
        vehicles_details.crew = request_body["crew"]
    if "passengers" in request_body:
        vehicles_details.passengers = request_body["passengers"]
    if "max_atmosphering_speed" in request_body:
        vehicles_details.max_atmosphering_speed = request_body["max_atmosphering_speed"]
    if "cargo_capacity" in request_body:
        vehicles_details.cargo_capacity = request_body["cargo_capacity"]
    if "consumables" in request_body:
        vehicles_details.consumables = request_body["consumables"]

    vehicles_details.update()

    return jsonify({"msg": "Updated"}), 200


@app.route("/vehicles/details/<int:vehicle_uid>", methods=["DELETE"])
def delete_vehicle_details(vehicle_uid):
    vehicle_details = Vehicles_Details.query.filter_by(
        uid=vehicle_uid).first()

    if vehicle_details is None:
        raise APIException("Vehicle Details not found", status_code=400)

    vehicle_details.delete()
    return jsonify({"msg": "Completed"}), 200


# <-- Favorites -->

@app.route("/user/favorites/<int:user_id>", methods=["GET"])
def get_favorites(user_id):
    favorite_characters = Favorite_Characters.query.filter_by(user_id=user_id)
    all_characters_favorites = list(
        map(lambda characters: characters.serialize, favorite_characters))

    favorite_planets = Favorite_Planets.query.filter_by(user_id=user_id)
    all_planets_favorites = list(
        map(lambda planets: planets.serialize, favorite_planets))

    favorite_vehicles = Favorite_Vehicles.query.filter_by(user_id=user_id)
    all_vehicles_favorites = list(
        map(lambda vehicles: vehicles.serialize, favorite_vehicles))

    response_body = {
        "favorites": {
            "characters": all_characters_favorites,
            "planets": all_planets_favorites,
            "vehicles": all_vehicles_favorites
        }
    }

    return jsonify(response_body), 200

# <-- Favorite Characters -->


@app.route("/favorite/characters/<int:user_id>", methods=["POST"])
def post_favorite_characters(user_id):
    request_body = request.get_json(silent=True)

    if "character_id" not in request_body:
        raise APIException("Character id is requerid", status_code=400)

    favorite_characters = Favorite_Characters(
        user_id=user_id,
        character_id=request_body["character_id"]
    )

    favorite_characters.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/favorite/characters/<int:user_id>/<int:character_id>", methods=["DELETE"])
def delete_favorite_character(user_id, character_id):
    favorite_character = Favorite_Characters.query.filter_by(
        user_id=user_id, character_id=character_id).first()

    if favorite_character is None:
        return jsonify({"error": "Favorite character not found"}), 404

    favorite_character.delete()

    return jsonify({"message": "Favorite character removed"}), 200

# <-- Favorite Planets -->


@app.route("/favorite/planets/<int:user_id>", methods=["POST"])
def post_favorite_planets(user_id):
    request_body = request.get_json(silent=True)

    if "planet_id" not in request_body:
        raise APIException("Planet id is requerid", status_code=400)

    favorite_planets = Favorite_Planets(
        user_id=user_id,
        planet_id=request_body["planet_id"]
    )

    favorite_planets.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/favorite/planets/<int:user_id>/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(user_id, planet_id):
    favorite_planet = Favorite_Planets.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()

    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    favorite_planet.delete()

    return jsonify({"message": "Favorite planet removed"}), 200

# <-- Favorite Vehicles -->


@app.route("/favorite/vehicles/<int:user_id>", methods=["POST"])
def post_favorite_vehicles(user_id):
    request_body = request.get_json(silent=True)

    if "vehicle_id" not in request_body:
        raise APIException("Vehicle id is requerid", status_code=400)

    favorite_vehicles = Favorite_Vehicles(
        user_id=user_id,
        vehicle_id=request_body["vehicle_id"]
    )

    favorite_vehicles.add()

    return jsonify({"msg": "Completed"}), 201


@app.route("/favorite/vehicles/<int:user_id>/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(user_id, vehicle_id):
    favorite_vehicle = Favorite_Vehicles.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()

    if favorite_vehicle is None:
        return jsonify({"error": "Favorite vehicle not found"}), 404

    favorite_vehicle.delete()

    return jsonify({"message": "Favorite vehicle removed"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
