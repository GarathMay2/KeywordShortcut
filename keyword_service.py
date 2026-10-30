# This file will be the program that runs the microservice and the Flask instance
# Check README for detailed information on how to get things running locally

from flask import Flask

app = Flask(__name__)
app.config["SERVICE_NAME"] = "Keyword Lookup Microservice"

@app.route("/")
def home():
    return {"message": "Keyword microservice is running!"}