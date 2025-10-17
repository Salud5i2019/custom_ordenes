from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# Usuario de ejemplo (puedes conectar con DB si quieres luego)
USERS = {
    "admin": "1234"
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify(msg="Credenciales inválidas"), 401
