from flask import Flask
from flask_cors import CORS
from app.routes.reservation_routes import reservation_routes  # Import your blueprint

# Create the Flask app
app = Flask(__name__)

# Enable CORS
#CORS(app)
CORS(app, resources={r"/api/*": {"origins": ["http://capstone-lms-frontend-bucket.s3-website-us-east-1.amazonaws.com"]}})

# Register your blueprint
app.register_blueprint(reservation_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)