from app import app
from flask import render_template, request, redirect, session
import user_commands
import recipe_commands
import shopping_list

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
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if user_commands.add_user(username, password1, "user"):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/addrecipe", methods=["GET", "POST"])
def addrecipe():
    #TODO: change required role to editor once course is over!
    if not user_commands.check_role("user"):
        return render_template("error.html", message="Tämä toimii vain kirjautuneilla käyttäjillä")

    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
        user_commands.check_csrf()
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        steps = request.form["steps"]
        if recipe_commands.add_recipe(name, ingredients, steps):
            return redirect("/")
        else:
            return render_template("error.html", message="Reseptin lisäys ei onnistunut")

@app.route("/viewrecipes")
def viewrecipes():
    recipe_list = recipe_commands.list_recipes()
    return render_template("viewrecipes.html", recipes=recipe_list)

@app.route("/recipe/<int:id>")
def recipe(id):
    name = recipe_commands.get_recipe_name(id)
    ingredient_list = recipe_commands.list_ingredients(id)
    step_list = recipe_commands.list_steps(id)
    return render_template("recipe.html", id=id, name=name, ingredients=ingredient_list, steps=step_list)

@app.route("/addtolist/<int:id>")
def addtolist(id):
    if shopping_list.add_to_list(id):
        return redirect("/viewrecipes")
    return render_template("error.html", message="Ostoslistalle lisäys ei onnistunut. Tämä toimii vain kirjautuneilla käyttäjillä")

@app.route("/shoppinglist", methods=["GET", "POST"])
def shoppinglist():
    if not user_commands.check_role("editor"):
        return render_template("error.html", message="Tämä toimii vain kirjautuneilla käyttäjillä")

    if request.method == "GET":
        current_list = shopping_list.get_shopping_list()
        return render_template("shoppinglist.html", current_list=current_list)
    if request.method == "POST":
        user_commands.check_csrf()
        shopping_list.remove_from_list(request.form.getlist("current_items"))
        return redirect("/shoppinglist")

@app.route("/adminview/<int:type>")
def adminview(type):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message="Ethän vain yrittänyt pääkäyttäjätoimintoihin ilman oikeuksia?")
    
    if type == 1:
        title = "user"
        adminlist = user_commands.list_users()
    if type == 2:
        title = "ingredient"
        adminlist = recipe_commands.list_all_ingredients()
    if type == 3:
        title = "unit"
        adminlist = recipe_commands.list_all_units()
    if type == 4:
        title = "recipe"
        adminlist = recipe_commands.list_recipes()

    return render_template("adminview.html", title=title, adminlist=adminlist)

@app.route("/deleteuser/<int:id>", methods=["POST"])
def deleteuser(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message="Ethän vain yrittänyt pääkäyttäjätoimintoihin ilman oikeuksia?")
    user_commands.check_csrf()
    
    if user_commands.delete_user(id):
        return redirect("/adminview/1")
    return render_template("error.html", message="Käyttäjän poisto ei onnistunut")

@app.route("/deleteingredient/<int:id>", methods=["POST"])
def deleteingredient(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message="Ethän vain yrittänyt pääkäyttäjätoimintoihin ilman oikeuksia?")
    user_commands.check_csrf()

    if recipe_commands.delete_ingredient(id):
        return redirect("/adminview/2")
    return render_template("error.html", message="Ainesosan poisto ei onnistunut")


@app.route("/deleteunit/<int:id>", methods=["POST"])
def deleteunit(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message="Ethän vain yrittänyt pääkäyttäjätoimintoihin ilman oikeuksia?")
    user_commands.check_csrf()

    if recipe_commands.delete_unit(id):
        return redirect("/adminview/3")
    return render_template("error.html", message="Yksikön poisto ei onnistunut")

@app.route("/deleterecipe/<int:id>", methods=["POST"])
def deleterecipe(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message="Ethän vain yrittänyt pääkäyttäjätoimintoihin ilman oikeuksia?")
    user_commands.check_csrf()

    if recipe_commands.delete_recipe(id):
        return redirect("/adminview/4")
    return render_template("error.html", message="Reseptin poisto ei onnistunut")


