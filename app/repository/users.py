"""
This file handles the data storage and retrieval for the user data using the database.
It defines methods for creating, retrieving, updating, and deleting user data.
It interacts with the database to store and retrieve data.
"""
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class UsersRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db      # db resource will be injected when this repository is created in the main.py

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

    def get_report(self, user_uid: str, report_uid: str):
        # TODO: Improve this ?
        try:
            user_dict = self.get_user(user_uid)
            return user_dict['reports'][report_uid]
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_user(self, user: dict):
        table = self.__db.Table('Users')        
        response = table.put_item(Item=user)    
        return response                         

    def user_exists(self, uid: str) -> bool:
        try:
            table = self.__db.Table('Users')
            response = table.get_item(Key={'uid': uid})
            return 'Item' in response  # return True if the user exists, False otherwise
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_report(self, user_uid: str, new_report: dict):
        if not self.user_exists(user_uid):
            self.create_user({'uid': user_uid, 'fname': 'None', 'lname': 'None', 'reports': {}})

        # TODO: Improve this ?
        table = self.__db.Table('Users')
        response = table.update_item(
            Key={'uid': user_uid},
            UpdateExpression='SET #reports.#rid = :new_report',
            ExpressionAttributeNames={
                '#reports': 'reports',
                '#rid': new_report.get('rid'),
            },
            ExpressionAttributeValues={
                ':new_report': new_report,
            },
            ConditionExpression=Key('uid').eq(user_uid),    # ensure that the user exists
            ReturnValues='ALL_NEW',
        )
        return response

    def update_user(self, user: dict):
        # TODO: Fix this, it is not working currently
        table = self.__db.Table('Users')    # referencing to table Users
        response = table.update_item(       # update single item
            Key={'uid': user.get('uid')},   # using partition key specifying which attributes will get updated
            UpdateExpression="""                
                set
                    fname=:fname,
                    lname=:lname,
                    reports=:reports,
            """,
            ExpressionAttributeValues={     # values defined in here will get injected to update expression
                ':fname': user.get('fname'),
                ':lname': user.get('lname'),
                ':reports': user.get('reports'),
            },
            ReturnValues="UPDATED_NEW"      # return the newly updated data point
        )
        return response

    def delete_user(self, uid: str):
        table = self.__db.Table('Users')    # referencing to table Users
        response = table.delete_item(       # delete user using uuid
            Key={'uid': uid}
        )
        return response