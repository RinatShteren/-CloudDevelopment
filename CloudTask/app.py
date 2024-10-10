
import json
import time
import os
import boto3
from botocore.exceptions import ClientError

# יצירת לקוח SNS לפרסום הודעות
sns_client = boto3.client('sns', region_name='us-east-1')

# משתנה שמכיל את מספר העבודות המותרות בו זמנית לכל משתמש
NUM_OF_CONCURRENT_JOBS = int(os.getenv('NumOfConcurrentJobs', 5))

# רשימה לדוגמה של העבודות הפעילות (לצורך הדגמה בלבד)
active_jobs = {}

def lambda_handler(event, context):
    try:
        # פירוק גוף הבקשה
        body = json.loads(event['body'])
        delay = body.get('delay')
        user_id = body.get('user_id')

        if not delay or not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid input, "delay" and "user_id" are required.'})
            }

        # בדיקת מספר העבודות הפעילות של המשתמש
        if active_jobs.get(user_id, 0) >= NUM_OF_CONCURRENT_JOBS:
            return {
                'statusCode': 429,
                'body': json.dumps({'message': 'Too many concurrent jobs for user.'})
            }

        # כאן תתבצע הלוגיקה להוספת עבודה חדשה (כמו שימוש ב-delay)
        # לצורך הפשטה, נניח שאנחנו רק מוסיפים את העבודה הפעילה למשתמש
        active_jobs[user_id] = active_jobs.get(user_id, 0) + 1

        # שליחת הודעה ל-SNS על השלמת עבודה
        topic_arn = os.getenv('SNS_TOPIC_ARN')  # קבלת ARN של ה-SNS ממשתנה סביבה
        if not topic_arn:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'SNS_TOPIC_ARN is not set in environment variables.'})
            }

        # פרסום הודעה ל-SNS
        sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps({'default': json.dumps({'user_id': user_id, 'message': 'Job completed'})}),
            Subject='Job Completion Notification',
            MessageStructure='json'
        )
        print(f'Successfully published message to SNS: {sns_client}')

        # תשובה של הצלחה
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Job submitted successfully and notification sent to SNS'})
        }

    except Exception as e:
        print(f'Failed to publish message to SNS: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def complete_job(user_id):
    """
    פונקציה שמסמלת את השלמת העבודה ושליחת הודעה ל-SNS Topic
    """
    try:
        # כאן העבודה מסתיימת ומורידים את כמות העבודות הפעילות
        active_jobs[user_id] = max(active_jobs.get(user_id, 1) - 1, 0)

        # פרסום הודעה ל-SNS Topic
        sns_response = sns_client.publish(
            TopicArn=os.getenv('JobCompletionTopicArn'),
            Message=json.dumps({'user_id': user_id, 'message': 'Job completed'}),
            Subject='Job Completed Notification'
        )
        print(f'Successfully published message to SNS: {sns_response}')

    except ClientError as e:
        print(f'Failed to publish message to SNS: {e}')