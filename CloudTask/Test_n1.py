import unittest
from datetime import datetime, timedelta
from FirstLambda import lambda_handler
from datetime import datetime, timezone


# Sending 5 requests from the same user with a 3-second delay;
# the test should pass since this is a permitted action
class TestConcurrentRequests(unittest.TestCase):

    def test_concurrent_requests(self):
        # Send 5 requests with a 3-second delay
        requests = [
            {'user_id': 'test1',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i)).isoformat() + 'Z',
             'delay': 3}
            for i in range(5)
        ]

        responses = []

        for request in requests:
            response = lambda_handler(request, None)
            responses.append(response)

        # Print responses
        print("Responses:")
        for i, response in enumerate(responses):
            print(f"Request {i + 1}: Status Code: {response['statusCode']}, Body: {response['body']}")

        # Verify that all responses have status code 200
        for response in responses:
            self.assertEqual(response['statusCode'], 200)  # Expect success


if __name__ == '__main__':
    unittest.main()
