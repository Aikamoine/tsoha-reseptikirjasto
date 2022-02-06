from sqlalchemy import null
from db import db

def add_recipe(name, ingredients, steps):
    if not check_length([(name, 30), (ingredients, 500), (steps, 1000)]):
        return False
    
    #TODO: make list_steps and list_ingredients -functions
    #TODO: remove empty strings/rows
    #TODO: handle ingredient inputs not consisting of 3 words
    ingredient_list = ingredients.split("\n")
    for i in range(len(ingredient_list)):
        #[amount, unit, name], replace unit and name with respective id's
        parts = ingredient_list[i].replace("\r", "").split(" ")
        parts[0] = float(parts[0].replace(",", "."))
        parts[1] = get_unit_id(parts[1])
        parts[2] = get_ingredient_id(parts[2])
        ingredient_list[i] = parts
    
    step_list = steps.split("\n")
    for step in step_list:
        step = step.replace("\r","")

    try:
        sql = """INSERT INTO recipes (name, visible) VALUES (:name, 1) RETURNING id"""
        recipe_id = db.session.execute(
            sql, {"name": name}).fetchone()[0]

        for ingredient in ingredient_list:
            sql = """INSERT INTO recipe_ingredients (recipe_id, ingredient_id, unit_id, amount) VALUES (:recipe_id, :ingredient_id, :unit_id, :amount) RETURNING id"""
            ing_id = db.session.execute(sql, {
                               "recipe_id": recipe_id,
                               "ingredient_id": ingredient[2],
                               "unit_id": ingredient[1],
                               "amount": ingredient[0]
                               }).fetchone()[0]
        
        for i in range(len(step_list)):
            sql = """INSERT INTO recipe_steps (recipe_id, step, number) VALUES (:recipe_id, :step, :number) RETURNING id"""
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
            sql = """INSERT INTO ingredients (name, visible) VALUES (:name, 1) RETURNING id"""
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
            sql = """INSERT INTO units (name, visible) VALUES (:name, 1) RETURNING id"""
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
    sql = "SELECT id, name, servings, time FROM recipes WHERE visible = 1 ORDER BY name DESC"
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
