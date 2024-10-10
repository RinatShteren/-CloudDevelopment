import json
import boto3
import os  #use for NumOfConcurrentJobs

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserRequests')
lambda_client = boto3.client('lambda')

#NumOfConcurrentJobs = 5
NumOfConcurrentJobs = int(os.environ.get('NUM_OF_CONCURRENT_JOBS', 5))  # ערך ברירת מחדל 5

def lambda_handler(event, context):
    test_user_id = 'c137d9f5-3f40-49ab-b966-f994deb939c0'
    delay = 42
    try:
        # ניסיון לקבל את הפריט הקיים
        response = table.get_item(Key={'user_id': test_user_id})

        if 'Item' in response:
            # אם הפריט קיים, עדכן את ה-request_count
            current_count = response['Item']['request_count']

            if current_count >= NumOfConcurrentJobs:
                # אם ה-request_count גבוה מהגבלה, החזר שגיאה
                return {
                    'statusCode': 429,
                    'body': json.dumps({
                        'message': 'Too many requests. You have reached the limit of concurrent requests.'
                    })
                }


            table.update_item(
                Key={'user_id': test_user_id},
                UpdateExpression="SET request_count = :val",
                ExpressionAttributeValues={
                    ':val': current_count + 1
                }
            )
            # שליחת קריאה לפונקציה השנייה אחרי עדכון
            payload = {
                'body': json.dumps({
                    'request_id': 'some-request-id',
                    'user_id': test_user_id,
                    'delay': delay  # אפשר לשנות את ה-delay לפי הצורך
                })

            }
            lambda_client.invoke(
                FunctionName='CloudTask-send_event',  # שם הפונקציה השנייה
                InvocationType='Event',  # קריאה אסינכרונית
                Payload=json.dumps(payload)
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Request count updated! and second Lambda invoked!',
                    'data': {
                        'user_id': test_user_id,
                        'request_count': float(current_count + 1)  # המרה ל-float
                    }
                })
            }
        else:
            # אם הפריט לא קיים, צור פריט חדש
            table.put_item(
                Item={
                    'user_id': test_user_id,
                    'delay': delay,
                    'request_count': 1
                }
            )
            # שליחת קריאה לפונקציה השנייה
            payload = {
                'body': json.dumps({
                    'request_id': 'some-request-id',
                    'user_id': test_user_id,
                    'delay': delay  # אפשר לשנות את ה-delay לפי הצורך
                })
            }
            lambda_client.invoke(
                FunctionName='YourSecondLambdaFunction',  # שם הפונקציה השנייה
                InvocationType='Event',  # קריאה אסינכרונית
                Payload=json.dumps(payload)
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'New item created and second Lambda invoked!',
                    'data': {
                        'user_id': test_user_id,
                        'request_count': 1
                    }
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
