from flask import Flask
from app.routes.user_routes import user_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Register routes
    app.register_blueprint(user_routes, url_prefix='/api')

    return app
