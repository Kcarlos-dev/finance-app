from flask import Blueprint, request, jsonify
from service.Validator.rules import validate_register
from database.user.sql_user import create_user_db
from service.util.password_hash import hash_password
users = Blueprint("users", __name__)

@users.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    errors = validate_register(data)
    
    if errors.get("error") == True:
        return jsonify({"error": errors.get("message")}), 400

    password_hash = hash_password(data.get("password"))
    data["password"] = password_hash

    create_user_db(data)

    return jsonify({"message": errors.get("message")}), 201

@users.route("/login", methods=["POST"])
def login():
    data = request.json
    return jsonify({"message": "User logged in successfully"}), 200