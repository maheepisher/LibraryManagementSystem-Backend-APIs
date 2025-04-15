from app.utils.db_connection import get_db_connection
import boto3
import json

# Initialize Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

def trigger_lambda(email):
    """
    Trigger the Lambda function with an email address.
    
    Args:
        email (str): The email address to pass to the Lambda function.
    
    Returns:
        dict: The response from the Lambda function.
    """
    try:
        # Prepare the event payload (mimicking API Gateway structure)
        payload = {
            'body': json.dumps({'email': email})
        }

        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName='CreateCustomerLambda',  # Replace with your Lambda function name
            InvocationType='RequestResponse',    # Synchronous invocation
            Payload=json.dumps(payload)          # Convert payload to JSON string
        )

        # Parse and return the Lambda response
        response_payload = response['Payload'].read().decode('utf-8')
        return json.loads(response_payload)

    except Exception as e:
        print(f"Error invoking Lambda: {str(e)}")
        return None


def manage_user_details(method, user_role, user_id=None, name=None, dob=None, address=None, email=None, phone_no=None):
    conn = get_db_connection()
    if conn is None or not conn.is_connected():
        print("Failed to establish database connection.")
        return {'Message': 'Database connection failed.'}

    cursor = None
    
    try:
        cursor = conn.cursor(dictionary=True)
        params = [method, user_role, user_id, name, dob, address, email, phone_no]
        cursor.callproc('ManageUserDetails', params)

        result = []
        for res in cursor.stored_results():
            result = res.fetchall()

        return result if result else {'Message': 'Operation completed but no data returned.'}
    except Exception as e:
        print(f"Error: {e}")
        return {'Message': 'Error processing request.'}
    finally:
        cursor.close()
        conn.close()
