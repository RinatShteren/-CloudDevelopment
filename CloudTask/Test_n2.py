import unittest
from datetime import datetime, timedelta
from FirstLambda import lambda_handler
from datetime import datetime, timezone
# Sending 6 identical requests with a 10-second delay,
# the sixth request is expected to fail since this is not a legal operation
class TestConcurrentRequests(unittest.TestCase):

    def test_concurrent_requests(self):
        # Send 6 requests with a 10-second delay
        requests = [
            {'user_id': 'test1',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i)).isoformat() + 'Z',
             'delay': 10}
            for i in range(6)
        ]
        responses = []

        for request in requests:
            response = lambda_handler(request, None)
            responses.append(response)

        # Print responses
        print("Responses:")
        for i, response in enumerate(responses):
            print(f"Request {i + 1}: Status Code: {response['statusCode']}, Body: {response['body']}")

        # Expect failure for the sixth request
        for response in responses:
            self.assertEqual(response['statusCode'], 200)  # Expect failure


if __name__ == '__main__':
    unittest.main()
