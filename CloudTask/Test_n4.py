import unittest
from datetime import datetime, timedelta
from FirstLambda import lambda_handler
import uuid
import random
from datetime import timezone

# Sending 20 requests with 4 different user names and a delay between 1 to 5 seconds.
# The requests succeed because they meet the system's conditions.
class TestConcurrentRequests(unittest.TestCase):

    def test_concurrent_requests(self):
        users = [str(uuid.uuid4()) for _ in range(4)]
        requests = []
        total_requests = 20

        for _ in range(total_requests):
            user_id = random.choice(users)
            delay = random.randint(1, 5)
            current_time = (datetime.now(timezone.utc) - timedelta(seconds=random.randint(1, 5))).isoformat() + 'Z'
            requests.append({
                'user_id': user_id,
                'current_time': current_time,
                'delay': delay
            })

        responses_by_user = {user: [] for user in users}
        start_time = datetime.now(timezone.utc)

        # Send and categorize responses by user
        for request in requests:
            response = lambda_handler(request, None)
            user_id = request['user_id']
            responses_by_user[user_id].append({
                'request': request,
                'response': response
            })

        # Print formatted report
        print("\n" + "=" * 60)
        print(f"Concurrent Requests Report - {total_requests} Requests")
        print("=" * 60)

        for user_id, responses in responses_by_user.items():
            print(f"\nUser ID: {user_id}")
            print("-" * 60)
            for i, data in enumerate(responses):
                request = data['request']
                response = data['response']
                delay = request['delay']
                request_time = request['current_time']
                response_time = datetime.now(timezone.utc).isoformat() + 'Z'
                duration = datetime.fromisoformat(response_time[:-1]) - datetime.fromisoformat(request_time[:-1])

                print(f"Request {i + 1}:")
                print(f"  ➔ Request Time: {request_time}")
                print(f"  ➔ Delay: {delay} seconds")
                print(f"  ➔ Response Time: {response_time}")
                print(f"  ➔ Duration: {duration.total_seconds():.2f} seconds")
                print(f"  ➔ Status Code: {response['statusCode']}")
                print(f"  ➔ Message: {response['body']}")
                print("-" * 60)

        end_time = datetime.now(timezone.utc)
        total_duration = (end_time - start_time).total_seconds()
        print(f"\nTotal time for all requests: {total_duration:.2f} seconds")
        print("=" * 60)


if __name__ == '__main__':
    unittest.main()
