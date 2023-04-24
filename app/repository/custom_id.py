from boto3.resources.base import ServiceResource
from app.repository.base_repository import BaseRepository

class CustomIdRepository(BaseRepository):
    def __init__(self, db: ServiceResource, table_name: str, table_key: str, custom_id_function: callable) -> None:
        super().__init__(db, table_name, table_key)
        self.__custom_id_function = custom_id_function

    # Override create method to use custom id function
    def create_id(self, item):
        self.__custom_id_function(self, item)

def custom_label_id(self, item):
    item['lid'] = str((self.count() + 1) * 10)

def custom_question_id(self, item):
    item['qid'] = str(self.count() + 1)

def custom_report_id(self, item):
    item['rid'] = str(self.count() + 1)