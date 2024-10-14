import json
import boto3
import os  #use for NumOfConcurrentJobs

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserRequests')
lambda_client = boto3.client('lambda')

NumOfConcurrentJobs =5 #int(os.environ.get('NUM_OF_CONCURRENT_JOBS', 5))

def lambda_handler(event, context):

    try:
        """  # בדיקה אם יש מפתח 'body' באירוע
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing body in event'})
            }

        body = json.loads(event['body'])  # קבלת ה-body מהבקשה
        print("Parsed body: " + json.dumps(body))  # הדפסת ה-body לאחר פענוח
        user_id = body.get('user_id')  # קבלת user_id מה-body
        delay = body.get('delay', 2)  # קבלת delay מה-body, אם לא נשלח יקבל ערך ברירת מחדל
        """
        #user_id = event.get('user_id')  # קבלת user_id מהבקשה
        #delay = event.get('delay', 2)  # קבלת delay מהבקשה, אם לא נשלח יקבל ערך ברירת מחדל
        #user_id = event.get('user_id')  # קבלת user_id מהבקשה
        #delay = event.get('delay', 42)  # קבלת delay מהבקשה, אם לא נשלח יקבל ערך ברירת מחדל
        user_id = event['queryStringParameters'].get('user_id')
        delay = event['queryStringParameters'].get('delay', 42)

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'user_id is required',
                    'user_id': event.get('user_id', user_id)  # הוספת user_id שנשלח בבקשה
                })
                #'body': json.dumps({'error': 'user_id is required'})
            }
        # ניסיון לקבל את הפריט הקיים
        response = table.get_item(Key={'user_id': user_id})

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
                Key={'user_id': user_id},
                UpdateExpression="SET request_count = :val",
                ExpressionAttributeValues={
                    ':val': current_count + 1
                }
            )
            # שליחת קריאה לפונקציה השנייה אחרי עדכון
            payload = {
                'body': json.dumps({
                    'request_id': 'some-request-id',
                    'user_id': user_id,
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
                        'user_id': user_id,
                        'request_count': float(current_count + 1)  # המרה ל-float
                    }
                })
            }
        else:
            # אם הפריט לא קיים, צור פריט חדש
            table.put_item(
                Item={
                    'user_id': user_id,
                    'delay': delay,
                    'request_count': 1
                }
            )
            # שליחת קריאה לפונקציה השנייה
            payload = {
                'body': json.dumps({
                    'request_id': 'some-request-id',
                    'user_id': user_id,
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
                    'message': 'New item created and second Lambda invoked!',
                    'data': {
                        'user_id': user_id,
                        'request_count': 1
                    }
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
