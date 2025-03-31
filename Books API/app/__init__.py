from flask import Flask
from app.routes.books_routes import books_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Register routes
    app.register_blueprint(books_routes, url_prefix='/api')

    return app