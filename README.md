# Cloud Task Manager

Cloud Task Manager is an AWS Lambda-based system designed to manage concurrent user requests. It handles user jobs with delays, utilizes DynamoDB for request tracking, and invokes subsequent Lambda functions based on certain conditions.

## Features

- Manage up to 5 concurrent user requests with delay-based handling.
- AWS Lambda and API Gateway integration.
- DynamoDB used to store user request data.
- Second Lambda function invoked after a request is added.
- Basic rate limiting to avoid exceeding concurrent job limits.

## Technologies Used

- AWS Lambda
- AWS API Gateway
- AWS DynamoDB
- Python (with `boto3` for AWS SDK)
- Unit testing with Python's `unittest` module

## Prerequisites

- AWS account with proper permissions to manage Lambda, API Gateway, and DynamoDB.
- AWS SAM CLI installed. You can install it from [AWS SAM CLI Installation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
- Python 3.x installed locally.

## Unit Tests

The project includes a series of unit tests designed to ensure the correctness of the lambda functions and their behavior under various conditions. The tests are written using Python's `unittest` module and provide broad coverage for the key functions in the project.
