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
        #reservation_id = payload.get('ReservationID')

        # Validate required fields
        if not all([operation, book_name, customer_email]):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields in payload'})
            }

        # Define email content based on Operation
        if operation.lower() == 'request':
            subject = 'LMS - Community Book Request'
            body = f"Your request to submit Community Book: {book_name} has been sent to library. Please wait till the decision is made."

        elif operation.lower() == 'approve':
            subject = 'LMS - Community Book Request Approved'
            body = f"Your request to submit Community Book: {book_name} has been approved by library. You can submit the book at the reception reception. Congratulations, you earned 100 points for this book."

        elif operation.lower() == 'decline':
            subject = 'LMS - Community Book Request Declined'
            body = f"Your request to submit Community Book: {book_name} has been declined by library. Please contact the library for details."

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