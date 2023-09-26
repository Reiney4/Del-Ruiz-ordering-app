from flask import Flask

def create_app():

    app = Flask(__name__)

    # add routes
    from app import routes
    
    return app
