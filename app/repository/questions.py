"""
This file handles storing and retrieving question data to and from the database.
It interacts with the domain layer to receive question data and return database responses.
"""
from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

class QuestionsRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table('Questions')    
        response = table.scan()             
        return response.get('Items', [])    

    def get_question(self, qid: str):
        try:
            table = self.__db.Table('Questions')                
            response = table.get_item(Key={'qid': qid})     
            return response['Item']                         
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_question(self, question: dict):
        table = self.__db.Table('Questions')        
        response = table.put_item(Item=question)    
        return response                

    def delete_user(self, qid: str):
        table = self.__db.Table('Questions')
        response = table.delete_item(
            Key={'qid': qid}
        )
        return response         
