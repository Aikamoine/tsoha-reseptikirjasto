from unittest import result
from sqlalchemy import null
from db import db

def add_recipe(name, servings, time):
    try:
        sql = "SELECT 1 FROM recipes WHERE name=:name"
        if db.session.execute(sql, {"name": name}).fetchone():
            return 0

        sql = "INSERT INTO recipes (name, servings, time, visible) VALUES (:name, :servings, :time, 1) RETURNING id"
        id = db.session.execute(
            sql, {"name": name, "servings": servings, "time": time}).fetchone()[0]

        db.session.commit()
        return id
    except:
        return 0

def add_tags(recipe_id, tag_string):
    tag_list = tag_string.replace(" ", "").replace("\r", "").split(",")
    for tag in tag_list:
        tag_id = get_tag_id(tag)
        try:
            sql = "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (:recipe_id, :tag_id)"
            db.session.execute(sql, {"recipe_id" : recipe_id, "tag_id": tag_id})
            db.session.commit()
        except:
            return False
    return True

def get_tag_id(tag):
    tag = tag.lower()
    try:
        sql = "SELECT id, tag FROM tags WHERE tag=:tag"
        result = db.session.execute(sql, {"tag": tag}).fetchone()

        if result:
            return result[0]

        sql = "INSERT INTO tags (tag) VALUES (:tag) RETURNING id"
        id = db.session.execute(sql, {"tag": tag}).fetchone()[0]
    except:
        return 0
    db.session.commit()
    return id

def add_ingredients(recipe_id, ingredient_string):
    ingredient_list = ingredients_from_string(ingredient_string)
    for ingredient in ingredient_list:
        try:
            sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, unit_id, amount) VALUES (:recipe_id, :ingredient_id, :unit_id, :amount)"
            db.session.execute(sql, {
                "recipe_id": recipe_id,
                "ingredient_id": ingredient[2],
                "unit_id": ingredient[1],
                "amount": ingredient[0]
            })    
        except:
            return False
    db.session.commit()
    return True

def add_steps(recipe_id, steps_string):
    step_list= steps_string.split("\n")

    for i in range(len(step_list)):
        step = step_list[i].replace("\r", "")
        try:
            sql = "INSERT INTO recipe_steps (recipe_id, step, number) VALUES (:recipe_id, :step, :number)"
            db.session.execute(sql, {
                "recipe_id": recipe_id,
                "step": step,
                "number": i})
        except:
            return False
    db.session.commit()
    return True

def ingredients_from_string(text):
    ingredient_list = text.split("\n")
    for i in range(len(ingredient_list)):
      #[amount, unit, name], replace unit and name with respective id's
        parts = ingredient_list[i].replace("\r", "").split(" ")

       #assume that an article with just one word is 'to taste'
        if len(parts) == 1:
            parts = ["1", "maunmukaan", parts[0]]

        #assume that an article without unit is one piece
        if len(parts) == 2:
            parts = [parts[0], "kpl", parts[1]]

        parts[0] = float(parts[0].replace(",", "."))
        parts[1] = get_unit_id(parts[1])
        parts[2] = get_ingredient_id(parts[2])
        ingredient_list[i] = parts
    return ingredient_list

def get_ingredient_id(name):
    name = name.lower()
    try:
        sql = "SELECT id, name, visible FROM ingredients WHERE name=:name"
        result = db.session.execute(sql, {"name": name}).fetchone()
        if result:
            return result[0]
        else:
            sql = "INSERT INTO ingredients (name, visible) VALUES (:name, 1) RETURNING id"
            ingredient_id = db.session.execute(sql, {"name": name}).fetchone()[0]
    except:
        return False
    db.session.commit()
    return ingredient_id


def get_unit_id(name):
    name = name.lower()
    try:
        sql = "SELECT id, name, visible FROM units WHERE name=:name"
        result = db.session.execute(sql, {"name": name}).fetchone()
        if result:
            return result[0]
        else:
            sql = "INSERT INTO units (name, visible) VALUES (:name, 1) RETURNING id"
            unit_id = db.session.execute(
                sql, {"name": name}).fetchone()[0]
    except:
        return False
    db.session.commit()
    return unit_id


def get_recipe_name(id):
    sql = "SELECT name FROM recipes WHERE id=:id"
    return db.session.execute(sql, {"id": id}).fetchone()[0]

def list_recipes():
    sql = "SELECT id, name, COALESCE(servings, 0) as servings, COALESCE(time, '') as time, tags FROM recipes " \
        "LEFT JOIN (SELECT RT.recipe_id as recipe_id, STRING_AGG(T.tag,', ') as tags FROM tags T, recipe_tags RT " \
        "WHERE T.id=RT.tag_id GROUP BY 1) T ON recipes.id=T.recipe_id WHERE visible = 1"
    result = db.session.execute(sql).fetchall()
    return result

def list_ingredients(id):
    sql = "SELECT RI.id, " \
	    "CASE WHEN RI.amount % 1 = 0 THEN RI.amount:: INTEGER ELSE RI.amount END as amount, " \
	    "U.name as unit, I.name as name " \
        "FROM recipe_ingredients RI " \
        "LEFT JOIN units U ON RI.unit_id=U.id " \
        "LEFT JOIN ingredients I ON RI.ingredient_id=I.id " \
        "WHERE RI.recipe_id=:id ORDER BY RI.id ASC"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def list_steps(id):
    sql = "SELECT id, step, number+1 as order FROM recipe_steps WHERE recipe_id=:id ORDER BY number ASC"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def list_all_ingredients():
    try:
        sql = "SELECT i.id, i.name, COUNT(ri.ingredient_id) as amt FROM recipe_ingredients ri " \
            "LEFT JOIN ingredients i ON i.id = ri.ingredient_id " \
            "GROUP BY i.id, i.name ORDER BY i.name"
        result = db.session.execute(sql)
    except:
        return False
    return result

def list_all_units():
    try:
        sql = "SELECT i.name, COUNT(ri.ingredient_id) as amt FROM recipe_ingredients ri " \
            "LEFT JOIN ingredients i ON i.id = ri.ingredient_id " \
            "GROUP BY i.name ORDER BY i.name"
        result = db.session.execute(sql)
    except:
        return False
    return result

def get_comments(id):
    sql = "SELECT U.username as name, C.id as id, C.stars as stars, C.comment as text FROM " \
        "comments C, users U WHERE C.user_id=U.id AND C.recipe_id=:id AND c.visible=1"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def get_average_stars(id):
    sql = "SELECT ROUND(AVG(stars), 1) as avg, COUNT(stars) FROM comments WHERE recipe_id=:id AND visible=1"
    result = db.session.execute(sql, {"id": id}).fetchone()
    print(result)
    return result

def add_comment(recipe_id, user_id, stars, comment_text):
    try:
        sql = "INSERT INTO comments (user_id, recipe_id, stars, comment, visible) VALUES " \
            "(:user_id, :recipe_id, :stars, :comment, 1)"
        db.session.execute(sql, {
            "user_id": user_id,
            "recipe_id": recipe_id,
            "stars": stars,
            "comment": comment_text})
        db.session.commit()
    except:
        return False
    return True

def update_recipe_ingredient(id, new_value):
    try:
        print("alku")
        sql = "SELECT id FROM ingredients WHERE name=:name"
        result = db.session.execute(sql, {"name": new_value}).fetchone()
        if result:
            new_id = result[0]
        else:
            print("else")
            sql = "INSERT INTO ingredients (name, visible) VALUES (:name, 1) RETURNING id"
            new_id = db.session.execute(sql, {"name": new_value}).fetchone()[0]
        print(f"new_id {new_id}")
        sql = "UPDATE recipe_ingredients SET ingredient_id=:new_id WHERE ingredient_id=:id"
        db.session.execute(sql, {"id": id, "new_id": new_id})

        print("update")
        sql = "DELETE FROM recipe_ingredients WHERE ingredient_id=:id"
        db.session.execute(sql, {"id": id})
        print("delete")
        db.session.commit()
    except:
        return False
    return True

def delete_recipe_step(step_id):
    try:
        sql = "SELECT recipe_id, number FROM recipe_steps WHERE id=:id"
        result = db.session.execute(sql, {"id": step_id}).fetchone()
        
        sql = "DELETE FROM recipe_steps WHERE id=:id"
        db.session.execute(sql, {"id": step_id})

        sql = "UPDATE recipe_steps SET number = number-1 WHERE recipe_id=:recipe_id AND number>=:number"
        db.session.execute(sql, {"recipe_id": result[0], "number": result[1]})
        db.session.commit()
    except:
        return False
    return True

def delete_comment(comment_id):
    try:
        sql = "UPDATE comments SET visible=0 WHERE id=:id"
        db.session.execute(sql, {"id": comment_id})
        db.session.commit()
    except:
        return False
    return True

def full_delete_recipe(id):
    try:

        #TODO: figure out how to ON DELETE CASCADE this...
        sql = "DELETE FROM recipe_steps WHERE recipe_id=:id"
        db.session.execute(sql, {"id": id})

        sql = "DELETE FROM recipe_ingredients WHERE recipe_id=:id"
        db.session.execute(sql, {"id": id})

        sql = "DELETE FROM comments WHERE recipe_id=:id"
        db.session.execute(sql, {"id": id})

        sql = "DELETE FROM recipe_tags WHERE recipe_id=:id"
        db.session.execute(sql, {"id": id})

        sql = "DELETE FROM recipes WHERE id=:id"
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
    return True

def delete_unit(id):
    try:
        sql = "UPDATE units SET visible=0 WHERE id=:id"
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
    return True

def delete_recipe(id):
    try:
        sql = "UPDATE recipes SET visible=0 WHERE id=:id"
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
    return True
