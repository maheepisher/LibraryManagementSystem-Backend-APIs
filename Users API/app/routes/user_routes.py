from flask import Blueprint, request, jsonify
from app.services.user_service import manage_user_details
from app.services.user_service import trigger_lambda
import json
user_routes = Blueprint('user_routes', __name__)



@user_routes.route('/user/test', methods=['GET'])
def test():
    # email_to_test = "maheepchawla97@gmail.com"
    # result = trigger_lambda(email_to_test)
    
    # if result:
    #     print("Lambda Response:")
    #     #print(json.dumps(result, indent=2))
    #     return jsonify({'Message': json.dumps(result, indent=2)})
    # else:
    #     print("Failed to get a response from Lambda")
    #     return jsonify({'Message': 'Failed to get a response from Lambda'})
    return jsonify({'Message': 'This Users API is Working!'})

# --------------------------- GET User Details ---------------------------
@user_routes.route('/user', methods=['GET'])
def get_user():
    user_role = request.args.get('role')
    user_id = request.args.get('id')

    if not user_role or not user_id:
        return jsonify({'Message': 'User role and ID are required for GET'}), 400

    result = manage_user_details('GET', user_role, user_id)
    return jsonify(result), 200 if result else 500

# --------------------------- POST (Create User) ---------------------------
@user_routes.route('/user', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ['role', 'name', 'dob', 'address', 'email', 'phone_no']

    if not all(field in data for field in required_fields):
        #return jsonify({'Message': 'All fields are required for creating a user'}), 400
        return jsonify({data}), 400

    result = manage_user_details('POST', data['role'], None, data['name'], data['dob'], data['address'], data['email'], data['phone_no'])
    if result:
        result1 = trigger_lambda(data['email'])
    
    return jsonify(result), 201 if result else 500

# --------------------------- PUT (Update User) ---------------------------
@user_routes.route('/user', methods=['PUT'])
def update_user():
    data = request.json
    required_fields = ['role', 'id', 'name', 'dob', 'address', 'email', 'phone_no']

    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'All fields are required for updating a user'}), 400

    result = manage_user_details('PUT', data['role'], data['id'], data['name'], data['dob'], data['address'], data['email'], data['phone_no'])
    return jsonify(result), 200 if result else 500

# --------------------------- DELETE (Remove User) ---------------------------
@user_routes.route('/user', methods=['DELETE'])
def delete_user():
    data = request.json
    if 'role' not in data or 'id' not in data:
        return jsonify({'Message': 'User role and ID are required for DELETE'}), 400

    result = manage_user_details('DELETE', data['role'], data['id'])
    return jsonify(result), 200 if result else 500
