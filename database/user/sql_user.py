import csv
import json
import random
import logging
from database.user.mysql_connect import connect_database

def get_users_db(email_user):
    try:
        conn = connect_database()
        if not email_user:
            return {"error": "email é obrigatório"}
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email_user,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

def create_user_db(data):
    try:
        conn = connect_database()
        if not data["email"] or not data["password"] or not data["name"]:
            return {"error": "email, password e name são obrigatórios"}
        cursor = conn.cursor()
        if len(get_users_db(data["email"])) > 0:
            return False
        cursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (data["email"], data["password"], data["name"]))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        return {"error": str(e)}
