import json
import boto3
from botocore.exceptions import ClientError

# Initialize SES client (v1)
ses_client = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # Parse the event body
        body = json.loads(event.get('body', '{}'))
        email_address = body.get('email')

        # Validate email address
        if not email_address or '@' not in email_address:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid or missing email address'})
            }

        # Verify email identity (SES v1)
        response = ses_client.verify_email_identity(
            EmailAddress=email_address
        )

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully requested verification for {email_address}',
                'response': response
            })
        }

    except ClientError as e:
        # Handle AWS SES errors
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to verify SES email identity',
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