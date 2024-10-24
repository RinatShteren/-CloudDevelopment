import unittest
from datetime import datetime, timedelta
from FirstLambda import lambda_handler
from datetime import datetime, timezone

# Sending 6 requests with a 5-second delay,
# the request is expected to succeed since this is a legal operation

class TestConcurrentRequests(unittest.TestCase):

    def test_concurrent_requests(self):
        # Send 6 requests with a 5-second delay
        requests = [
            {'user_id': 'test1',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i)).isoformat() + 'Z',
             'delay': 5}
            for i in range(6)
        ]

        responses = []

        for request in requests:
            response = lambda_handler(request, None)
            responses.append(response)

        print("Responses:")
        for i, response in enumerate(responses):
            print(f"Request {i + 1}: Status Code: {response['statusCode']}, Body: {response['body']}")

        # Expect success for each request
        for response in responses:
            self.assertEqual(response['statusCode'], 200)  # Expect success


if __name__ == '__main__':
    unittest.main()
