from app import app
from flask import render_template, request, redirect, session
import user_commands
import recipe_commands

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
        return redirect("/")

    #username = request.form["username"]
    #password = request.form["password"]
    # TODO: check username and password
    #session["username"] = username
    #return redirect("/")

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
    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
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
    ingredient_list = recipe_commands.list_ingredients(id)
    step_list = recipe_commands.list_steps(id)
    return render_template("recipe.html", ingredients=ingredient_list, steps=step_list)

@app.route("/logout")
def logout():
    user_commands.logout()
    return redirect("/")
