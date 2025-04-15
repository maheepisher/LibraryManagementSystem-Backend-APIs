from flask import Blueprint, request, jsonify
from app.services.reservation_service import manage_reservation_details
from app.services.reservation_service import trigger_reservation_lambda
import json

reservation_routes = Blueprint('reservation_routes', __name__)

@reservation_routes.route('/reservation/test', methods=['GET'])
def test():
    # result = trigger_reservation_lambda("REQUEST", "BOOK ABC", "maheep.isher@gmail.com", 16)
    
    # if result:
    #     print("Lambda Response:")
    #     #print(json.dumps(result, indent=2))
    #     return jsonify({'Message': json.dumps(result, indent=2)})
    # else:
    #     print("Failed to get a response from Lambda")
    #     return jsonify({'Message': 'Failed to get a response from Lambda'})
        #return jsonify({'Message': 'This Users API is Working!'})
    return jsonify({'Message': 'This Reservation API is working!'})

@reservation_routes.route('/reservation/reserve', methods=['POST'])
def reserve_book():
    data = request.json
    if 'role' not in data or 'book_id' not in data or 'customer_id' not in data:
        return jsonify({'Message': 'User role, Book ID, and Customer ID are required for RESERVE'}), 400

    result = manage_reservation_details('RESERVE', data['role'], None, data['book_id'], data['customer_id'], None, None)
    if isinstance(result, list) and len(result) == 1:
        print(f"Book name: {data['book_name']}, Customer email: {data['customer_email']}, Reservation ID: {result[0]['ReservationID']}")
        result2 = trigger_reservation_lambda('REQUEST', data['book_name'], data['customer_email'], result[0]['ReservationID'])
        return jsonify(result[0]), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500

# --------------------------- Fetch My Reservations ---------------------------
@reservation_routes.route('/reservation', methods=['GET'])
def get_reservations():
    role = request.args.get('role')
    customer_id = request.args.get('customer_id', type=int)
    if not role or customer_id is None:
        return jsonify({'Message': 'User role and Customer ID are required'}), 400

    result = manage_reservation_details('GETRESERVATION', role, None, None, customer_id)
    if isinstance(result, list):
        return jsonify(result), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500


# --------------------------- Fetch Reservation Requests - ADMIN ---------------------------
@reservation_routes.route('/reservation/requests', methods=['GET'])
def get_requests():
    role = request.args.get('role')
    
    if not role:
        return jsonify({'Message': 'User role is required'}), 400

    result = manage_reservation_details('FETCHREQUESTS', role, None, None, None)
    if isinstance(result, list):
        return jsonify(result), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500
    
#-----Approve/Decline Reservation Requests
@reservation_routes.route('/reservation/requests', methods=['PUT'])
def request_decision():
    data = request.json
    required_fields = ['role', 'reservation_id', 'approver_id', 'decision']

    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'Reservation ID, Approver ID & Decision are required for updating a decision'}), 400

    result = manage_reservation_details('REQUESTDECISIONS', data['role'], data['reservation_id'], None, None, data['decision'], data['approver_id'])
    if result:
        print(f"decision: {data['decision']}, bookname: {data['book_name']}, email: {data['customer_Email']}, id: {data['reservation_id']}")
        result1 = trigger_reservation_lambda(data['decision'], data['book_name'], data['customer_Email'], data['reservation_id'])
    return jsonify(result), 200 if result else 500

# --------------------------- Fetch Returns ---------------------------
@reservation_routes.route('/reservation/returns', methods=['GET'])
def get_return_req():
    role = request.args.get('role')
    customer_id = request.args.get('customer_id', type=int)
    if not role or customer_id is None:
        return jsonify({'Message': 'User role and Customer ID are required'}), 400

    result = manage_reservation_details('RETURNREQ', role, None, None, customer_id)
    if isinstance(result, list):
        return jsonify(result), 200
    elif isinstance(result, dict) and 'Message' in result:
        return jsonify(result), 500 if 'error' in result['Message'].lower() else 200
    else:
        return jsonify({'Message': 'Unexpected response from database'}), 500
    
    
    #-----Manage Book Returns
@reservation_routes.route('/reservation/returns', methods=['PUT'])
def handle_returns():
    data = request.json
    required_fields = ['role', 'reservation_id', 'approver_id']

    if not all(field in data for field in required_fields):
        return jsonify({'Message': 'Reservation ID, Approver ID & Decision are required for updating a decision'}), 400

    result = manage_reservation_details('RETURNS', data['role'], data['reservation_id'], None, None, None, data['approver_id'])
    return jsonify(result), 200 if result else 500
