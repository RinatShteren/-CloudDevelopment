import unittest
from datetime import datetime, timedelta
from FirstLambda import lambda_handler
from datetime import timezone
from time import sleep


# Sending 10 requests (5 with 6 seconds delay and 5 with 3 seconds delay);
# some requests will succeed, and others will not.
class TestConcurrentRequests(unittest.TestCase):

    def test_concurrent_requests(self):
        # Create 5 requests with a 6-second delay
        requests_10_seconds = [
            {'user_id': 'test2',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i)).isoformat() + 'Z',
             'delay': 10}
            for i in range(5)
        ]


        requests_3_seconds = [
            {'user_id': 'test2',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i + 5)).isoformat() + 'Z',
             'delay': 3}
            for i in range(2)
        ]

        sleep(10)

        requests_8_seconds = [
            {'user_id': 'test2',
             'current_time': (datetime.now(timezone.utc) - timedelta(seconds=i + 5)).isoformat() + 'Z',
             'delay': 8}
            for i in range(3)
        ]
        responses = []

        # Combine all requests
        all_requests = requests_10_seconds + requests_3_seconds+requests_8_seconds

        # Send the requests and store the responses
        for request in all_requests:
            response = lambda_handler(request, None)
            responses.append({
                'request': request,
                'response': response
            })

        # Print formatted report
        print("\n" + "=" * 60)
        print(f"Concurrent Requests Report - {len(all_requests)} Requests")
        print("=" * 60)

        for i, data in enumerate(responses):
            request = data['request']
            response = data['response']
            delay = request['delay']
            status = "Accepted" if response['statusCode'] == 200 else "Rejected"
            request_time = request['current_time']

            print(f"Request {i + 1}:")
            print(f"  ➔ Request Time: {request_time}")
            print(f"  ➔ Delay: {delay} seconds")
            print(f"  ➔ Status: {status}")
            print("-" * 60)

        # Count accepted and rejected requests
        accepted_requests = len([res for res in responses if res['response']['statusCode'] == 200])
        rejected_requests = len(responses) - accepted_requests

        print(f"\nTotal Accepted Requests: {accepted_requests}")
        print(f"Total Rejected Requests: {rejected_requests}")
        print("=" * 60)


if __name__ == '__main__':
    unittest.main()
