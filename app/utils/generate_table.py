"""
This file contains code to create the database table for the application.
It is typically run once when setting up the application.
"""
'''
This file handles connecting to the DynamoDB database.
'''
import os
import boto3
import pathlib
from dotenv import load_dotenv
from boto3.resources.base import ServiceResource

base_dir = pathlib.Path(__file__).parent.parent.parent
load_dotenv(base_dir.joinpath('.env'))
DB_REGION_NAME = os.getenv('DB_REGION_NAME')
DB_ACCESS_KEY_ID = os.getenv('DB_ACCESS_KEY_ID')
DB_SECRET_ACCESS_KEY = os.getenv('DB_SECRET_ACCESS_KEY')

def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
        endpoint_url='http://localhost:8000',     # uncomment if using local dynamodb
        region_name=DB_REGION_NAME,
        aws_access_key_id=DB_ACCESS_KEY_ID,
        aws_secret_access_key=DB_SECRET_ACCESS_KEY)
    return ddb

def generate_table(ddb, table_name, table_key):
    ddb.create_table(
        TableName=table_name,
        AttributeDefinitions=[{
            'AttributeName': table_key,     # In this case, I only specified uid as partition key (there is no sort key)
            'AttributeType': 'S'        # with type string
        }],
        KeySchema=[{
            'AttributeName': table_key,     # attribute uid serves as partition key
            'KeyType': 'HASH'
        }],
        ProvisionedThroughput={         # specifying read and write capacity units
            'ReadCapacityUnits': 10,    # these two values really depend on the app's traffic
            'WriteCapacityUnits': 10
        }
    )

tables = [
    ('Users', 'uid'),
    ('Surveys', 'sid'),
    ('Reports', 'rid'),
    ('Labels', 'lid'),
    ('Questions', 'qid')
]

ddb = initialize_db()
for table_name, table_key in tables:
    generate_table(ddb, table_name, table_key)