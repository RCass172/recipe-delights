import os
from flask import (
    Flask, render_template, redirect, url_for, session, request, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
# Imports the env package as it is hidden and not pushed to GitHub
if os.path.exists("env.py"):
    import env


# Creates an instance of Flask
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Global variable used for categories to work on base.html
# https://liutheprogrammer.wordpress.com/2019/09/18/flask-templates-define-global-variables-for-template-usage/
@app.context_processor
def category():
    categories = list(mongo.db.categories.find())
    return dict(categories=categories)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if the username entered already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry! Username already exists, please choose again")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Puts the new user into session
        session["user"] = request.form.get("username").lower()
        flash("Registration has been successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if the username entered already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure the password matches
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))
            else:
                # Invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        user_recipes = list(
            mongo.db.recipes.find({"created_by": session["user"]}))
        return render_template(
            "profile.html", username=username, user_recipes=user_recipes)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user from session
    flash("You have successfully been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/recipe_categories")
def recipe_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("recipes.html", categories=categories)


@app.route("/full_category/<category_id>")
def full_category(category_id):
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    recipes = mongo.db.recipes.find(
        {"category_name": category["category_name"]})
    return render_template(
        "full_category.html", category=category, recipes=recipes)


@app.route("/full_recipe/<recipe_id>")
def full_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        "full_recipe.html", recipe=recipe)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_img": request.form.get("recipe_img"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.getlist("method"),
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Your recipe has been successfully added")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("add_recipe.html")


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe has been deleted successfully")
    return redirect(url_for('profile', username=session["user"]))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "recipe_img": request.form.get("recipe_img"),
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.getlist("method"),
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edit)
        flash("Recipe has been updated successfully")
        return redirect(url_for('profile', username=session["user"]))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=recipe)


# How and where to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
