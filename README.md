# FastAPI Backend

This is the backend API for EVA, using FastAPI and Python.

## Overview

The most significant file is the GPT handler, which is responsible for handling all prompts,
decoding all responses, and building the report. It can be found [here](/app/utils/gpt_handler.py).
Additionally, the entire prompting behavior is configurable and can be modified by changing the
values in the config directory found [here](/app/config).

## Resources

[FastAPI Docs](https://fastapi.tiangolo.com/)
[Local DynamoDB (Part 1)](https://medium.com/nerd-for-tech/introduction-to-fastapi-and-local-dynamodb-595c990ed0f8)
[Local DynamoDB (Part 2)](https://medium.com/nerd-for-tech/python-fastapi-with-aws-dynamodb-931073a87a52)

## Local Setup

Before starting, make sure you have Python 3.9.

1. Create a new virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```

2. Install the required Python libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Add your environment variables. For example:

    ```text
    PORT=5000
    DB_REGION_NAME="us-east-1"
    DB_ACCESS_KEY_ID="..."
    DB_SECRET_ACCESS_KEY="..."
    OPENAI_API_KEY="..."
    CLIENT_ORIGIN_URL="http://localhost:3000"
    AUTH0_DOMAIN="...us.auth0.com"
    AUTH0_AUDIENCE="https://example.com"
    ```

4. Run the server:

    ```bash
    python main.py
    ```

5. Navigate to [http://localhost:5000/docs](http://localhost:5000/docs) to test that the server is working.

## Cloud Deployment

This project is deployed to AWS Lambda using the serverless library.
More information about how to do this will be added soon.
