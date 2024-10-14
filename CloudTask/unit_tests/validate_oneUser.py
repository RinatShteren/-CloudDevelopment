import unittest
import boto3


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True,True)  # add assertion here
    def test1(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('UserRequests')
        test_user_id = 'c137d9f5-3f40-49ab-b966-f994deb939c0'
        delay = 2
            # ניסיון לקבל את הפריט הקיים
        response = table.get_item(Key={'user_id': test_user_id})

        if 'Item' in response:
                # אם הפריט קיים, עדכן את ה-request_count
            current_count = response['Item']['request_count']


if __name__ == '__main__':
    unittest.main()
