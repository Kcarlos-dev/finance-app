import jwt
import datetime
from .config import get_config

def generate_token(user_id,email_user):
    try:
        payload = {
            "id": user_id,
            "email": email_user,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }
        encoded = jwt.encode(payload, get_config("JWT_SECRET"), algorithm="HS256")
        return encoded
    except Exception as e:
        return f"Erro ao gerar token: {e}"

def verify_token(token):
    try:
        payload = jwt.decode(token, get_config("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expirado"
    except jwt.InvalidTokenError:
        return "Token inválido"

