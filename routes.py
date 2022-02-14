from crypt import methods
from curses import ERR
from app import app
from flask import render_template, request, redirect, session
import user_commands
import recipe_commands
import shopping_list

ERRORS = {"not_logged_in": "Tämä toimii vain kirjautuneilla käyttäjillä",
          "admin_access" : "Tämä on sallittu vain pääkäyttäjälle",
          "adding_failed" : " lisäys ei onnistunut",
          "deleting_failed": " poisto ei onnistunut"}

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
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if user_commands.add_user(username, password1, "user"):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjän"+ERRORS["adding_failed"])

@app.route("/addrecipe", methods=["GET", "POST"])
def addrecipe():
    #TODO: change required role to editor once course is over!
    if not user_commands.check_role("user"):
        return render_template("error.html", message=ERRORS["not_logged_in"])

    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
        user_commands.check_csrf()
        name = request.form["name"]
        servings = request.form["servings"]
        time = request.form["time"]
        ingredients = request.form["ingredients"]
        steps = request.form["steps"]
        if recipe_commands.add_recipe(name, ingredients, steps, servings, time):
            return redirect("/")
        else:
            return render_template("error.html", message="Reseptin"+ERRORS["adding_failed"])

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
    return render_template("recipe.html", id=id, name=name, ingredients=ingredient_list, steps=step_list, comments=comments)

@app.route("/comment", methods=["POST"])
def comment():
    if not user_commands.check_role("user"):
        render_template("error.html", message=ERRORS["not_logged_in"])
    user_commands.check_csrf()

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        render_template("error.html", message="Virheellinen määrä tähtiä")
    
    comment_text = request.form["comment_text"]
    if len(comment_text) < 2 or len(comment_text) > 500:
        render_template("error.html", message="Liian lyhyt (2) tai pitkä (500) viesti")
    recipe_id = request.form["recipe_id"]

    if recipe_commands.add_comment(recipe_id, user_commands.user_id(), stars, comment_text):
        return redirect("/recipe/"+recipe_id)
    return render_template("error.html", message="Kommentin"+ERRORS["adding_failed"])

@app.route("/addtolist/<int:id>")
def addtolist(id):
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
    user_commands.check_csrf()
    shopping_list.reset_shopping_list()
    return redirect("/shoppinglist")

@app.route("/adminview/<int:type>")
def adminview(type):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])
    
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
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()
    
    if user_commands.delete_user(id):
        return redirect("/adminview/1")
    return render_template("error.html", message="Käyttäjän "+ERRORS["deleting_failed"])

@app.route("/deleteingredient/<int:id>", methods=["POST"])
def deleteingredient(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()

    if recipe_commands.delete_ingredient(id):
        return redirect("/adminview/2")
    return render_template("error.html", message="Ainesosan "+ERRORS["deleting_failed"])


@app.route("/deleteunit/<int:id>", methods=["POST"])
def deleteunit(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()

    if recipe_commands.delete_unit(id):
        return redirect("/adminview/3")
    return render_template("error.html", message="Yksikön "+ERRORS["deleting_failed"])

@app.route("/deleterecipe/<int:id>", methods=["POST"])
def deleterecipe(id):
    if not user_commands.check_role("admin"):
        return render_template("error.html", message=ERRORS["admin_access"])
    user_commands.check_csrf()

    if recipe_commands.delete_recipe(id):
        return redirect("/adminview/4")
    return render_template("error.html", message="Reseptin "+ERRORS["deleting_failed"])


