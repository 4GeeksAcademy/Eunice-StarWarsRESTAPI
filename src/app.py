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


@app.route("/characters/<int:character_uid>", methods=["GET"])
def get_characters_details(character_uid):
    characters = Characters_Details.query.filter_by(
        uid=character_uid).first()

    if not characters:
        response_body = {
            "msg": "No character details available."
        }
        return jsonify(response_body), 404 
    else:
        response_body = {
            "msg": "ok",
            "characters": characters.serialize()
        }
        return jsonify(response_body), 200


@app.route("/characters/details", methods=["POST"])
def post_character_details():
    request_body = request.get_json(silent=True)
    if request_body is None:
        raise APIException("You must send information!", status_code=400)
    if "uid" not in request_body:
        raise APIException("Uid is required", status_code=400)
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


""" @app.route("/characters/<int:character_uid>", methods=["PUT"])
def put_character_details(character_uid):
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
def delete_character_details(character_uid):
    character = Characters.query.filter_by(uid=character_uid).first()

    if character is None:
        raise APIException("Character not found", status_code=400)

    character.delete()
    return jsonify({"msg": "Completed"}), 200

 """
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

    planet.delete()
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


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
