import json
import time
import os
import boto3

EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME')
client = boto3.client('events')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    delay = body.get('delay', 0)
    request_id = body.get('request_id')
    user_id = body.get('user_id')

    if isinstance(delay, int) and delay > 0 and request_id and user_id:
        time.sleep(delay)

        response = client.put_events(
            Entries=[
                {
                    'Source': 'my.custom.source',
                    'DetailType': 'LambdaFunctionCompleted',
                    'Detail': json.dumps({
                        'message': 'Lambda function completed successfully',
                        'request_id': request_id,
                        'user_id': user_id
                    }),
                    'EventBusName': EVENT_BUS_NAME
                }
            ]
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Lambda function completed successfully', 'event_response': response})
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid delay, request_id, or user_id parameter'})
        }
