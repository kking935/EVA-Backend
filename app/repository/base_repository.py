from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError
from uuid import uuid4

class BaseRepository:
    def __init__(self, db: ServiceResource, table_name: str, table_key: str) -> None:
        self.__db = db
        self.__table_name = table_name
        self.__table_key = table_key

    def count(self):
        table = self.__db.Table(self.__table_name)
        response = table.scan(Select='COUNT')
        return response['Count']

    def get_all(self):
        table = self.__db.Table(self.__table_name)    
        response = table.scan()
        return response.get('Items', [])
    
    def get(self, id: str):
        try:
            table = self.__db.Table(self.__table_name)                
            response = table.get_item(Key={self.__table_key: id})     
            return response['Item']                         
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_id(self, item):
        item[self.__table_key] = str(uuid4())

    def create(self, item: dict):
        if self.__table_key not in item or not item[self.__table_key]:
            self.create_id(item)
        table = self.__db.Table(self.__table_name)        
        response = table.put_item(Item=item)
        return item   
    
    def update(self, item: dict):
        table = self.__db.Table(self.__table_name)
        update_expression = "set "
        expression_attribute_names = {}
        expression_attribute_values = {}
        for i, (key, value) in enumerate(item.items()):
            if key == self.__table_key:
                continue
            update_expression += f"#{key} = :{key}"
            expression_attribute_names[f"#{key}"] = key
            expression_attribute_values[f":{key}"] = value
            if i < len(item) - 1:
                update_expression += ", "
        response = table.update_item(
            Key={self.__table_key: item[self.__table_key]},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return self.get(item[self.__table_key])

    def delete(self, id: str):
        table = self.__db.Table(self.__table_name)
        response = table.delete_item(
            Key={self.__table_key: id}
        )
        return response   
