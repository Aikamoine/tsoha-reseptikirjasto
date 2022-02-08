import os
from flask import abort, request, session
from itsdangerous import exc
from sqlalchemy import null
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from shopping_list import reset_shopping_list

ROLES = {"none": 0, "user": 1, "editor": 2, "admin": 3}

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username AND visible = 1"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True


def logout():
    reset_shopping_list()
    del session["user_id"]
    del session["username"]
    del session["user_role"]
    del session["csrf_token"]
    
def add_user(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password, role)
                 VALUES (:username, :password, :role)"""
        db.session.execute(
            sql, {"username": username, "password": hash_value, "role": role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def list_users():
    try:
        sql = "SELECT id, username FROM users WHERE visible = 1"
        result = db.session.execute(sql)
    except:
        return False
    return result

def check_role(role):
    user_role = session.get("user_role", "none")
    return ROLES[user_role] >= ROLES[role]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def delete_user(id):
    if id == session["user_id"]:
        return False
    try:
        sql = "UPDATE users SET visible=0 WHERE id=:id"
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
    return True
