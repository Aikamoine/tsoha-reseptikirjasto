from sqlalchemy import null
from db import db

def add_recipe(name, ingredients, steps):
    if not check_length([(name, 30), (ingredients, 800), (steps, 2000)]):
        return False
    
    #TODO: make list_steps and list_ingredients -functions
    #TODO: remove empty strings/rows
    #TODO: handle ingredient inputs not consisting of 3 words
    ingredient_list = ingredients.split("\n")
    for i in range(len(ingredient_list)):
        #[amount, unit, name], replace unit and name with respective id's
        parts = ingredient_list[i].replace("\r", "").split(" ")

        #assume that an article with just one row is 'to taste'
        if len(parts) == 1:
            parts = ["1", "maunmukaan", parts[0]]

        #assume that an article without unit is one piece
        if len(parts) == 2:
            parts = [parts[0], "kpl", parts[1]]

        parts[0] = float(parts[0].replace(",", "."))
        parts[1] = get_unit_id(parts[1])
        parts[2] = get_ingredient_id(parts[2])
        ingredient_list[i] = parts
    
    step_list = steps.split("\n")
    for step in step_list:
        step = step.replace("\r","")

    try:
        sql = "INSERT INTO recipes (name, visible) VALUES (:name, 1) RETURNING id"
        recipe_id = db.session.execute(
            sql, {"name": name}).fetchone()[0]

        for ingredient in ingredient_list:
            sql = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, unit_id, amount) VALUES (:recipe_id, :ingredient_id, :unit_id, :amount) RETURNING id"
            ing_id = db.session.execute(sql, {
                               "recipe_id": recipe_id,
                               "ingredient_id": ingredient[2],
                               "unit_id": ingredient[1],
                               "amount": ingredient[0]
                               }).fetchone()[0]
        
        for i in range(len(step_list)):
            sql = "INSERT INTO recipe_steps (recipe_id, step, number) VALUES (:recipe_id, :step, :number) RETURNING id"
            step_id = db.session.execute(sql, {
                "recipe_id": recipe_id,
                "step": step_list[i],
                "number": i,
            }).fetchone()[0]

        db.session.commit()
    except:
        return False
    
    return recipe_id

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
    sql = "SELECT id, name, COALESCE(servings, 0) as servings, COALESCE(time, '') as time FROM recipes WHERE visible = 1 ORDER BY name DESC"
    result = db.session.execute(sql).fetchall()
    return result

def list_ingredients(id):
    sql = "SELECT RI.amount as amount, U.name as unit, I.name as name FROM " \
        "recipe_ingredients RI, units U, ingredients I WHERE RI.recipe_id=:id AND U.id=RI.unit_id AND I.id=RI.ingredient_id"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def list_steps(id):
    sql = "SELECT step, number+1 as order FROM recipe_steps WHERE recipe_id=:id ORDER BY number ASC"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def list_all_ingredients():
    try:
        sql = "SELECT id, name FROM ingredients WHERE visible = 1"
        result = db.session.execute(sql)
    except:
        return False
    return result

def list_all_units():
    try:
        sql = "SELECT id, name FROM units WHERE visible = 1"
        result = db.session.execute(sql)
    except:
        return False
    return result

def get_comments(id):
    sql = "SELECT U.username as name, C.stars as stars, C.comment as text FROM " \
        "comments C, users U WHERE C.user_id=U.id AND C.recipe_id=:id"
    result = db.session.execute(sql, {"id": id}).fetchall()
    return result

def add_comment(recipe_id, user_id, stars, comment_text):
    try:
        sql = "INSERT INTO comments (user_id, recipe_id, stars, comment, visible) VALUES " \
            "(:user_id, :recipe_id, :stars, :comment, 1)"
        print(
            f"INSERT INTO comments (user_id, recipe_id, stars, comment, visible) VALUES ({user_id}, {recipe_id}, {stars}, {comment_text}, 1)")
        db.session.execute(sql, {
            "user_id": user_id,
            "recipe_id": recipe_id,
            "stars": stars,
            "comment": comment_text})
        db.session.commit()
    except:
        return False
    return True

def check_length(tocheck):
    """Checks a list against maximum lenghts

    Args:
        tocheck ([list]): list of tuples, first value is text, second max length

    Returns:
        [boolean]: True, if all elements match their assigned max length
    """
    for element in tocheck:
        if len(element[0]) > element[1]:
            return False
    return True

def delete_ingredient(id):
    try:
        sql = "UPDATE ingredients SET visible=0 WHERE id=:id"
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
