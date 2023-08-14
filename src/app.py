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
from models import db, User, Characters
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route("/character", methods=["GET"])
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


@app.route("/character", methods=["POST"])
def post_chracter():
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


@app.route("/character/<int:character_uid>", methods=["PUT"])
def put_character(character_uid):
    request_body = request.get_json(silent=True)

    character = Characters.query.filter_by(uid=character_uid).first()
    
    if character is None:
        raise APIException("Character not found", status_code=400)
    if request_body is None:
        raise APIException("You must send new information", status_code=400)
    if "uid" in request_body:
        character.uid = request_body["uid"]
    if "name" in request_body:
        character.name = request_body["name"]
    if "url" in request_body:
        character.url = request_body["url"]
    
    character.update()
    
    return jsonify({"msg": "Updated"}), 200

@app.route("/character/<int:character_uid>", methods=["DELETE"])
def delete_character(character_uid):
    character = Characters.query.filter_by(uid=character_uid).first() 
    
    if character is None:
        raise APIException("Character not found", status_code=400)
    
    character.delete()
    return jsonify({"msg": "Completed"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
