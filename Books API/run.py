from flask import Flask
from flask_cors import CORS
from app.routes.books_routes import books_routes  # Import your blueprint

# Create the Flask app
app = Flask(__name__)

# Enable CORS
#CORS(app)
#CORS(app, resources={r"/api/*": {"origins": ["http://capstone-lms-frontend-bucket.s3-website-us-east-1.amazonaws.com"]}})
# Register your blueprint

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://capstone-lms-frontend-bucket.s3-website-us-east-1.amazonaws.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # If credentials are needed
    return response

app.register_blueprint(books_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)