# FastAPI Backend

This is the backend API for MASLOW, using FastAPI and Python.

## Resources

[FastAPI Docs](https://fastapi.tiangolo.com/)
[Local DynamoDB (Part 1)](https://medium.com/nerd-for-tech/introduction-to-fastapi-and-local-dynamodb-595c990ed0f8)
[Local DynamoDB (Part 2)](https://medium.com/nerd-for-tech/python-fastapi-with-aws-dynamodb-931073a87a52)

## Setup

Before starting, make sure you have Python 3.7 or above, npm 14 or above, and Docker installed on your machine.

1. Create a new virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```

2. Install the required Python libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Run DynamoDB locally using Docker:

    ```bash
    docker run -p 8000:8000 -d amazon/dynamodb-local
    ```

4. Install DynamoDB Admin globally on your machine (not the docker container) using npm:

    ```bash
    npm install -g dynamodb-admin
    ```

5. Configure the Dynamo endpoint to be the endpoint of the docker container:

    ```bash
    set DYNAMO_ENDPOINT=http://localhost:8000
    ```

6. Run DynamoDB Admin:

    ```bash
    dynamodb-admin
    ```

7. Navigate to [http://localhost:8001](http://localhost:8001) and confirm that you see the following view:

![Alt text](https://miro.medium.com/v2/resize:fit:720/format:webp/1*SOrhdTo_wpK4Yuj6XuGrFQ.png "DynamoDB Admin View")

## Execution

To run the server, execute the following command:

```bash
uvicorn main:app --reload
```

*Note: Including `--reload` above enables automatic reload*

### Interactive API Docs

To view automatic interactive API documentation using **Swagger-UI**, navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

To view automatic interactive API documentation using **ReDoc**, navigate to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
