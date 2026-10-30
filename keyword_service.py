# This file will be the program that runs the microservice and the Flask instance

from flask import Flask

app = Flask(__name__)
app.config["SERVICE_NAME"] = "Keyword Lookup Microservice"

@app.route("/")
def home():
    return {"message": "Keyword microservice is running!"}