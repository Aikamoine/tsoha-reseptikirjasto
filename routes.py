from contextlib import redirect_stdout
from crypt import methods
from ctypes.wintypes import tagSIZE
from email import contentmanager
from app import app
from flask import render_template, request, redirect, session
import user_commands
import recipe_commands
import shopping_list

ERRORS = {"not_logged_in": "Tämä toimii vain kirjautuneilla käyttäjillä",
          "admin_access" : "Tämä on sallittu vain pääkäyttäjälle",
          "adding_failed" : " lisäys ei onnistunut",
          "deleting_failed": " poisto ei onnistunut",
          "retrieval_failed": " tietojen haku ei onnistunut"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not user_commands.login(username, password):
            return render_template("error.html", message="Väärä tunnuksen ja salasanan kombo")
        return redirect("/viewrecipes")

@app.route("/logout")
def logout():
    shopping_list.reset_shopping_list()
    user_commands.logout()
    return redirect("/")

@app.route("/adduser", methods=["GET", "POST"])
def adduser():
    if request.method == "GET":
        return render_template("adduser.html")
    if request.method == "POST":        
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        length_check = check_length([
            (username, 3, 30),
            (password1, 8, 100)])
        if not length_check == "ok":
            return render_template("error.html", message=length_check)

        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if user_commands.add_user(username, password1, "user"):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjän"+ERRORS["adding_failed"])

@app.route("/addrecipe", methods=["GET", "POST"])
def addrecipe():
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["not_logged_in"])

    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
        user_commands.check_csrf()

        name = request.form["name"]
        servings = request.form["servings"]
        time = request.form["time"]
        tags = request.form["tags"]
        ingredients = request.form["ingredients"]
        steps = request.form["steps"]

        length_check = check_length([
            (name, 3, 30),
            (ingredients, 5, 800),
            (steps, 5, 2000),
            (time, 0, 20),
            (tags, 0, 50),
            (servings, 0, 20)])
        if not length_check=="ok":
            return render_template("error.html", message=length_check)

        recipe_id = recipe_commands.add_recipe(name, servings, time)
        if recipe_id == 0:
            return render_template("error.html", message=f"Reseptin {name} lisäys ei onnistunut. Tuplanimi tai tietokantahäiriö.")

        if not recipe_commands.add_tags(recipe_id, tags):
            return render_template("error.html", message="Tunnisteiden"+ERRORS["adding_failed"])

        if not recipe_commands.add_ingredients(recipe_id, ingredients):
            return render_template("error.html", message="Ainesosien"+ERRORS["adding_failed"])
        
        if not recipe_commands.add_steps(recipe_id, steps):
            return render_template("error.html", message="Työvaiheiden"+ERRORS["adding_failed"])

        return viewrecipes()

@app.route("/viewrecipes")
def viewrecipes():
    recipe_list = recipe_commands.list_recipes()
    return render_template("viewrecipes.html", recipes=recipe_list)

@app.route("/recipe/<int:id>")
def recipe(id):
    name = recipe_commands.get_recipe_name(id)
    ingredient_list = recipe_commands.list_ingredients(id)
    step_list = recipe_commands.list_steps(id)
    comments = recipe_commands.get_comments(id)
    average = recipe_commands.get_average_stars(id)
    return render_template("recipe.html", id=id, name=name, ingredients=ingredient_list, steps=step_list, comments=comments, avg=average)

@app.route("/comment", methods=["POST"])
def comment():
    if not user_commands.check_role("user"):
        render_template("error.html", message=ERRORS["not_logged_in"])
    user_commands.check_csrf()

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        render_template("error.html", message="Virheellinen määrä tähtiä")
    
    comment_text = request.form["comment_text"]

    length_check = check_length([(comment_text, 2, 500)])
    if not length_check == "ok":
        return render_template("error.html", message=length_check)

    recipe_id = request.form["recipe_id"]

    if recipe_commands.add_comment(recipe_id, user_commands.user_id(), stars, comment_text):
        return redirect("/recipe/"+recipe_id)
    return render_template("error.html", message="Kommentin"+ERRORS["adding_failed"])

@app.route("/addtolist/<int:id>")
def addtolist(id):
    if not user_commands.check_role("user"):
        render_template("error.html", message=ERRORS["not_logged_in"])

    if shopping_list.add_to_list(id):
        return redirect("/viewrecipes")
    return render_template("error.html", message=ERRORS["not_logged_in"])

@app.route("/shoppinglist", methods=["GET", "POST"])
def shoppinglist():
    if not user_commands.check_role("user"):
        return render_template("error.html", message=ERRORS["not_logged_in"])

    if request.method == "GET":
        current_list = shopping_list.get_shopping_list()
        return render_template("shoppinglist.html", current_list=current_list)
    if request.method == "POST":
        user_commands.check_csrf()
        shopping_list.remove_from_list(request.form.getlist("current_items"))
        return redirect("/shoppinglist")


@app.route("/clearlist", methods=["POST"])
def clearlist():
    if not user_commands.check_role("user"):
        render_template("error.html", message=ERRORS["not_logged_in"])

    user_commands.check_csrf()
    shopping_list.reset_shopping_list()
    return redirect("/shoppinglist")

@app.route("/editrecipe/<int:id>")
def editrecipe(id):
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])
    
    name = recipe_commands.get_recipe_name(id)
    ingredients = recipe_commands.list_ingredients(id)
    steps = recipe_commands.list_steps(id)
    comments = recipe_commands.get_comments(id)
    return render_template("editrecipe.html", id=id, name=name, ingredients=ingredients, steps=steps, comments=comments)


@app.route("/deleteingredient/<int:id>", methods=["POST"])
def deleteingredient(id):
    user_commands.check_csrf()
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if recipe_commands.delete_recipe_ingredient(request.form["ingredient_id"]):
        return redirect(f"/editrecipe/{id}")
    return render_template("error.html", message="Ainesosan "+ERRORS["deleting_failed"])

@app.route("/deletestep/<int:id>", methods=["POST"])
def deletestep(id):
    user_commands.check_csrf()
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if recipe_commands.delete_recipe_step(request.form["step_id"]):
        return redirect(f"/editrecipe/{id}")
    return render_template("error.html", message="Työvaiheen"+ERRORS["deleting_failed"])

@app.route("/deletecomment/<int:id>", methods=["POST"])
def deletecomment(id):
    user_commands.check_csrf()
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if recipe_commands.delete_comment(request.form["comment_id"]):
        return redirect(f"/editrecipe/{id}")
    return render_template("error.html", message="Työvaiheen"+ERRORS["deleting_failed"])


@app.route("/fulldelete/<int:id>", methods=["POST"])
def fulldelete(id):
    user_commands.check_csrf()
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if recipe_commands.full_delete_recipe(id):
        return redirect("/viewrecipes")
    return render_template("error.html", message="Reseptin"+ERRORS["deleting_failed"])

@app.route("/deleteusers/<int:id>", methods=["POST"])
def deleteusers(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()
    
    if user_commands.delete_user(id):
        return redirect("/edit/users")
    return render_template("error.html", message="Käyttäjän "+ERRORS["deleting_failed"])

@app.route("/edit/<string:subject>")
def edit(subject):
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if subject == "ingredients":
        content = recipe_commands.list_all_ingredients()

    if subject == "units":
        content = recipe_commands.list_all_units()

    if subject == "tags":
        content = recipe_commands.list_all_tags()

    if subject == "users":
        if not user_commands.check_role("admin"):
            return render_template("error.html", message=ERRORS["admin_access"])
        content = user_commands.list_users()
        return render_template("adminview.html", title=subject, adminlist=content)

    if subject == "recipes":
        content = recipe_commands.list_recipes()
        return render_template("adminview.html", title=subject, adminlist=content)

    if not content:
        return render_template("error.html", message=ERRORS["retrieval_failed"])

    return render_template("edit.html", title=subject, ingredients=content)

@app.route("/update/<string:subject>/<int:id>", methods=["POST"])
def update(subject, id):
    user_commands.check_csrf()
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])

    if subject == "ingredients":
        if recipe_commands.update_recipe_ingredient(id, request.form["new_value"]):
            return redirect(f"/edit/{subject}")

    if subject == "units":
        if recipe_commands.update_unit(id, request.form["new_value"]):
            return redirect(f"/edit/{subject}")

    if subject == "tags":
        if recipe_commands.update_tag(id, request.form["new_value"]):
            return redirect(f"/edit/{subject}")

    return render_template("error.html", message=ERRORS["deleting_failed"])

@app.route("/deleterecipes/<int:id>", methods=["POST"])
def deleterecipes(id):
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()

    if recipe_commands.delete_recipe(id):
        return redirect("/edit/recipes")
    return render_template("error.html", message="Reseptin "+ERRORS["deleting_failed"])

@app.route("/addingredients", methods=["POST"])
def addingredients():
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()
    ingredients = request.form["ingredients"]
    recipe_id = request.form["recipe_id"]
    if recipe_commands.add_ingredients(recipe_id, ingredients):
        return redirect(f"/editrecipe/{recipe_id}")
    return render_template("error.html", message=ERRORS["adding_failed"])

@app.route("/addsteps", methods=["POST"])
def addsteps():
    if not user_commands.check_role("editor"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()
    steps = request.form["steps"]
    recipe_id = request.form["recipe_id"]
    if recipe_commands.add_steps(recipe_id, steps):
        return redirect(f"/editrecipe/{recipe_id}")
    return render_template("error.html", message=ERRORS["adding_failed"])

def check_length(tocheck):
    """Checks a list against maximum lenghts

    Args:
        tocheck ([list]): list of tuples, which are (text, min_length, max_length)

    Returns:
        [boolean]: True, if all elements match their assigned max length
    """
    for element in tocheck:
        if len(element[0]) > element[2]:
            return f"syöte {element[0]} on liian pitkä, maksimi {element[2]}"
        if len(element[0]) < element[1]:
            return f"syöte {element[0]} on liian lyhyt, minimi {element[1]}"
    return "ok"
