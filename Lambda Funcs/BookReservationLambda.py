import json
import boto3
from botocore.exceptions import ClientError

# Initialize SES client
ses_client = boto3.client('ses', region_name='us-east-1')

# Sender email (must be verified in SES)
SENDER_EMAIL = "maheepchawla97@gmail.com"

def lambda_handler(event, context):
    try:
        # Parse the event payload
        payload = json.loads(event.get('body', '{}')) if 'body' in event else event
        operation = payload.get('Operation')
        book_name = payload.get('BookName')
        customer_email = payload.get('CustomerEmail')
        reservation_id = payload.get('ReservationID')

        # Validate required fields
        if not all([operation, book_name, customer_email, reservation_id]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields in payload'})
            }

        # Define email content based on Operation
        if operation.lower() == 'request':
            subject = 'LMS - Reservation Request'
            body = f"Your request for reservation of {book_name} has been sent to library. Your Reservation ID is {reservation_id}"

        elif operation.lower() == 'approved':
            subject = 'LMS - Reservation Request Approved'
            body = f"Reservation ID: {reservation_id}: Your request for reservation of {book_name} has been approved by library. You can pick up your book from reception."

        elif operation.lower() == 'declined':
            subject = 'LMS - Reservation Request Declined'
            body = f"Reservation ID: {reservation_id}: Your request for reservation of {book_name} has been declined by library. Please contact the library for details."

        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': f'Invalid Operation value: {operation}'})
            }

        # Send email via SES
        response = ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={
                'ToAddresses': [customer_email]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Email sent successfully to {customer_email} for {operation}',
                'response': response
            })
        }

    except ClientError as e:
        # Handle SES-specific errors
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to send email',
                'error': error_message
            })
        }
    except Exception as e:
        # Handle unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'An unexpected error occurred',
                'error': str(e)
            })
        }