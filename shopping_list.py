from recipe_commands import list_ingredients
from db import db
from flask import abort, request, session

current_list = {}

def add_to_list(id):
    to_add = list_ingredients(id)
    for ingredient in to_add:
        title = f"{ingredient[2]} {ingredient[3]}"
        try:
            sql = "SELECT amount FROM shoppinglists WHERE user_id=:user_id AND title=:title"
            result = db.session.execute(sql, {
                "user_id": session["user_id"],
                "title": title}).fetchone()
            if result == None:
                sql = """INSERT INTO shoppinglists (user_id, title, amount) VALUES (:user_id, :title, :amount)"""
                db.session.execute(sql, {
                    "user_id": session["user_id"],
                    "title": title,
                    "amount": ingredient[1]})

            else:
                sql = "UPDATE shoppinglists SET amount=:amount WHERE user_id=:user_id AND title=:title"
                db.session.execute(sql, {
                    "amount": result[0] + ingredient[1],
                    "user_id": session["user_id"],
                    "title": title})
        except:
            return False
    db.session.commit()
    return True

def get_shopping_list():
    sql = "SELECT CASE WHEN amount % 1 = 0 THEN amount:: INTEGER ELSE amount END as amount, title FROM shoppinglists WHERE user_id=:user_id"
    result = db.session.execute(sql, {
        "user_id": session["user_id"]}).fetchall()
    return result

def remove_from_list(to_remove):
    try:
        for title in to_remove:
            sql = "DELETE FROM shoppinglists where user_id=:user_id AND title=:title"
            db.session.execute(
                sql, {"user_id": session["user_id"], "title": title})
    except:
        return False
    db.session.commit()
    return True

def reset_shopping_list():
    try:
        sql = "DELETE FROM shoppinglists where user_id=:user_id"
        db.session.execute(
            sql, {"user_id": session["user_id"]})
    except:
        return False

    db.session.commit()
    return True
