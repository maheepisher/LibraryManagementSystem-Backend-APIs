from flask import Blueprint, request, jsonify
from app.services.books_service import manage_books_details

books_routes = Blueprint('books_routes', __name__)

# --------------------------- GET User Details ---------------------------
@books_routes.route('/books', methods=['GET'])
def get_books():
    # Extract query parameters
    user_role = request.args.get('role')
    book_id = request.args.get('book_id')
    bookName = request.args.get('BookName')
    genre = request.args.get('genre')
    author = request.args.get('author')

    # Validate required parameter
    if not user_role:
        return jsonify({'Message': 'User role is required'}), 400

    # Call the function to fetch books
    result = manage_books_details('GET', user_role, book_id, bookName, genre, author)

    # Check if result is an error message
    if isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500

    # Return the array of books
    return jsonify(result), 200


#---------------POST METHOD------------------------------
@books_routes.route('/books', methods=['POST'])
def add_book():
    data = request.json
    required_fields = ['role', 'BookName', 'Author', 'Genre', 'PublishDate', 'BookDescription', 'isCommunityBook']
    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'Missing required fields'}), 400

    result = manage_books_details('POST', data['role'], None, data['BookName'], data['Genre'], data['Author'], data['PublishDate'], data['BookDescription'], data['isCommunityBook'])
    return jsonify(result), 201 if result else 500

# --------------------------- DELETE (Remove User) ---------------------------
@books_routes.route('/books', methods=['DELETE'])
def delete_book():
    data = request.json
    if 'role' not in data or 'id' not in data:
        return jsonify({'Message': 'User role and Book ID are required for DELETE'}), 400

    result = manage_books_details('DELETE', data['role'], data['id'])
    return jsonify(result), 200 if result else 500


@books_routes.route('/books/community_book', methods=['POST'])
def add_community_book():
    data = request.json
    
    required_fields = ['role', 'BookName', 'Author', 'Genre', 'PublishDate', 'BookDescription', 'CustomerID']
    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'Missing required fields'}), 400

    result = manage_books_details('SHAREBOOK', data['role'], None, data['BookName'], data['Genre'], data['Author'], data['PublishDate'], data['BookDescription'], None, data['CustomerID'])
    return jsonify(result), 201 if result else 500

# --------------------------- GET User Details ---------------------------
@books_routes.route('/books/community_book', methods=['GET'])
def get_my_books():
    role = request.args.get('role')
    customer_id = request.args.get('customer_id', type=int)
    if not role or customer_id is None:
        return jsonify({'Message': 'User role and Customer ID are required'}), 400

    result = manage_books_details('GETMYSHAREDBOOKS', role, None, None, None, None, None, None, None, customer_id)
    if isinstance(result, list):
        return jsonify(result), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500
    
@books_routes.route('/books/community_book/requests', methods=['GET'])
def get_community_books_requests():
    role = request.args.get('role')
    if not role:
        return jsonify({'Message': 'User role is required'}), 400

    result = manage_books_details('COMMBOOKSREQ', role, None, None, None, None, None, None, None, None)
    if isinstance(result, list):
        return jsonify(result), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500
    
    #-----Approve/Decline Reservation Requests
@books_routes.route('/books/community_book/requests', methods=['PUT'])
def commBook_decision():
    data = request.json
    required_fields = ['role', 'BookName', 'CustomerID', 'AdminID', 'decision', 'requestDate']

    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'Reservation ID, Approver ID & Decision are required for updating a decision'}), 400

    result = manage_books_details('COMMBOOKDECISION', data['role'], None, data['BookName'], None, None, None, None, None, data['CustomerID'], data['AdminID'], data['decision'], data['requestDate'])
    return jsonify(result), 200 if result else 500