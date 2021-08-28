import os
from flask import (
    Flask, render_template, redirect, url_for, session, request)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# Imports the env package as it is hidden and not pushed to GitHub
if os.path.exists("env.py"):
    import env


# Creates an instance of Flask
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


# How and where to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
