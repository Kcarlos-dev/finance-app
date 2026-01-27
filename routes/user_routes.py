from flask import Blueprint, request, jsonify
from service.validator.rules import validate_register, validate_login
from database.user.sql_user import create_user_db, get_users_db
from service.util.password_hash import hash_password, check_password
from service.util.jwt_token import generate_token
users = Blueprint("users", __name__)

@users.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    errors = validate_register(data)
    
    if errors.get("error") == True:
        return jsonify({"error": errors.get("message")}), 400

    password_hash = hash_password(data.get("password"))
    data["password"] = password_hash

    result = create_user_db(data)
    if result == False:
        return jsonify({"error": "email já cadastrado"}), 400

    return jsonify({"message": errors.get("message")}), 201

@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    errors = validate_login(data)
    if errors.get("error") == True:
        return jsonify({"error": errors.get("message")}), 400

    user = get_users_db(data.get("email"))[0]
    print(user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password(data.get("password"), user.get("password")):
        return jsonify({"error": "Invalid password"}), 401

    token = generate_token(user.get("id"), user.get("email"))
    return jsonify({"message": "User logged in successfully", "token": token}), 200