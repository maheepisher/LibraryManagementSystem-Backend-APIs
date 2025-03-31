from flask import Flask
from app.routes.reservation_routes import reservation_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Register routes
    app.register_blueprint(reservation_routes, url_prefix='/api')

    return app
