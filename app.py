from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to the Cook It Up API!"