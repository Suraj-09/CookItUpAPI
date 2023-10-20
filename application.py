from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello():
    return 'Welcome to the Cook It Up API!'
