"""
This file handles storing and retrieving user data to and from the database.
It interacts with the domain layer to receive user data and return database responses.
"""
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class UsersRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table('Users')    
        response = table.scan()             
        return response.get('Items', [])    

    def get_user(self, uid: str):
        try:
            table = self.__db.Table('Users')                
            response = table.get_item(Key={'uid': uid})     
            return response['Item']                         
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_user(self, user: dict):
        table = self.__db.Table('Users')        
        response = table.put_item(Item=user)    
        return response                         

    def delete_user(self, uid: str):
        table = self.__db.Table('Users')
        response = table.delete_item(
            Key={'uid': uid}
        )
        return response