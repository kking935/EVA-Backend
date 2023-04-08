"""
This file handles storing and retrieving report data to and from the database.
It interacts with the domain layer to receive report data and return database responses.
"""
from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

class ReportsRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table('Reports')    
        response = table.scan()             
        return response.get('Items', [])    

    def get_report(self, rid: str):
        try:
            table = self.__db.Table('Reports')                
            response = table.get_item(Key={'rid': rid})     
            return response['Item']                         
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_report(self, report: dict):
        table = self.__db.Table('Reports')        
        response = table.put_item(Item=report)    
        return response                

    def delete_report(self, rid: str):
        table = self.__db.Table('Reports')
        response = table.delete_item(
            Key={'rid': rid}
        )
        return response         
