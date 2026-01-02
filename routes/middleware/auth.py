from functools import wraps
from flask import request, jsonify, g
from service.util.jwt_token import verify_token
from database.user.sql_user import get_users_db

def token_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Token não enviado"}), 401

            token = auth_header.split(" ", 1)[1]
            payload = verify_token(token)
            if isinstance(payload, str):
                return jsonify({"error": payload}), 401

            email = payload.get("email")
            user = get_users_db(email)
            if not user:
                return jsonify({"error": "Usuário não encontrado"}), 404
            if allowed_roles and user.get("auth") not in allowed_roles:
                return jsonify({"error": "Acesso negado"}), 403

            g.current_user = payload
            return view(*args, **kwargs)
        return wrapper
    return decorator