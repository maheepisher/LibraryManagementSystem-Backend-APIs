from flask import Flask
from flask_cors import CORS
from app.routes.user_routes import user_routes  # Import your blueprint

# Create the Flask app
app = Flask(__name__)

# Enable CORS
#CORS(app)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
# Register your blueprint

app.register_blueprint(user_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)