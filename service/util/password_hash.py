import logging
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    if not password:
        logging.error("Senha não informada")
        return False
    try:
        return generate_password_hash(password)
    except Exception as e:
        logging.error(f"Erro ao gerar hash da senha: {e}")
        return False

def check_password(password, hashed_password):
    if not password or not hashed_password:
        logging.error("Senha ou hash da senha não informada")
        return False
    try:
        return check_password_hash(hashed_password, password)
    except Exception as e:
        logging.error(f"Erro ao verificar senha: {e}")
        return False
