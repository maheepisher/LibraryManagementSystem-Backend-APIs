from app.utils.db_connection import get_db_connection
from app.utils.db_connection import get_db_connection
import boto3
import json

# Initialize Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

def trigger_reservation_lambda(operation, book_name, customer_email, reservation_id):
    """
    Trigger the Lambda function to send a reservation email via SES.
    
    Args:
        operation (str): The operation type ('Request', 'Approve', 'Decline').
        book_name (str): The name of the book being reserved.
        customer_email (str): The email address of the customer.
        reservation_id (str): The unique reservation ID.
    
    Returns:
        dict: The response from the Lambda function, or None if an error occurs.
    """
    try:
        # Prepare the event payload (mimicking API Gateway structure)
        payload = {
            'body': json.dumps({
                'Operation': operation,
                'BookName': book_name,
                'CustomerEmail': customer_email,
                'ReservationID': reservation_id
            })
        }

        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName='BookReservationLambda',  # Replace with your Lambda function name
            InvocationType='RequestResponse',      # Synchronous invocation
            Payload=json.dumps(payload)            # Convert payload to JSON string
        )

        # Parse and return the Lambda response
        response_payload = response['Payload'].read().decode('utf-8')
        return json.loads(response_payload)

    except Exception as e:
        print(f"Error invoking Lambda: {str(e)}")
        return None

def manage_reservation_details(operation, user_role, reservationID=None, bookID=None, customerID=None, decision = None, ApproverID = None):
    conn = get_db_connection()
    if conn is None or not conn.is_connected():
        print("Failed to establish database connection.")
        return {'Message': 'Database connection failed.'}

    cursor = None
    
    #cursor = conn.cursor(dictionary=True)
    try:
        cursor = conn.cursor(dictionary=True)
        params = [operation, user_role, reservationID, bookID, customerID, decision, ApproverID]
        cursor.callproc('ManageReservations', params)
        result = []
        for res in cursor.stored_results():
            result = res.fetchall()
        return result if result else {'Message': 'Operation completed but no data returned.'}
        #return result  # Return the entire list, empty or not
    except Exception as e:
        print(f"Error: {e}")
        return {'Message': f'Error processing request: {str(e)}'}
    finally:
        cursor.close()
        conn.close()
