import os
from flask import Flask
# Imports the env package as it is hidden and not pushed to GitHub
if os.path.exists("env.py"):
    import env


# Creates an instance of Flask
app = Flask(__name__)


# How and where to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
