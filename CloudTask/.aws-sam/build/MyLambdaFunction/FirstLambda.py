import json
import boto3
import os  # use for NumOfConcurrentJobs
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserRequests2')
lambda_client = boto3.client('lambda')

NumOfConcurrentJobs = int(os.environ.get('NUM_OF_CONCURRENT_JOBS', 5))

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    try:
       # user_id = event['queryStringParameters'].get('user_id')
        #delay = event['queryStringParameters'].get('delay', 2)
        user_id = event.get('user_id')
        delay = event.get('delay', 2)

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'user_id is required'})
            }

        current_time = datetime.utcnow().isoformat() + 'Z'
        current_time_obj = datetime.fromisoformat(current_time[:-1])

        # Search for the last 5 requests of the user
        response = table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={
                ':uid': user_id
            },
            Limit=5,
            ScanIndexForward=False  # to get the requests from newest to oldest
        )

        # Count the current requests, with a maximum of 5
        current_count = len(response['Items'])

        if current_count == NumOfConcurrentJobs:
            # If the current request count is equal to the limit
            # Check if there is a request whose delay has passed
            for item in response['Items']:
                delay_time = timedelta(seconds=float(item['delay']))
                end_time = datetime.fromisoformat(item['current_time'][:-1]) + delay_time
                if current_time_obj >= end_time:
                    # If the delay has passed, we can add a new request
                    current_count -= 1  # Decrease the count for the old request

        # If the current request count is below the limit
        if current_count < NumOfConcurrentJobs:
            # Add a new request
            table.put_item(
                Item={
                    'user_id': user_id,
                    'current_time': current_time,
                    'delay': delay,
                    'request_count': current_count + 1  # Update the request count
                }
            )

            # Send a call to the second function after the update
            payload = {
                'body': json.dumps({
                    'request_id': 'some-request-id',
                    'user_id': user_id,
                    'delay': delay  # Can change the delay as needed
                })
            }
            lambda_client.invoke(
                FunctionName='CloudTask-send_event',
                InvocationType='Event',
                Payload=json.dumps(payload)
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'New request added and second Lambda invoked!',
                    'data': {
                        'user_id': user_id,
                        'request_count': current_count + 1  # Update the count
                    }
                })
            }
        else:
            return {
                'statusCode': 429,
                'body': json.dumps({
                    'message': 'Too many requests. You have reached the limit of concurrent requests.'
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
