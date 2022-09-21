import time

from typing import TypedDict, Union

from utils.schemas import SchemaAbstract

class QOTDInfo(TypedDict):
    question: str

class QOTDSchema(SchemaAbstract.Schema):

    DB_NAME="QOTD"

    def __init__(self, question: str):
        self.question = question
    
    def insert(self) -> (str, dict):
        return '''
            INSERT
            INTO QOTD
            VALUES (:question)
        ''', {
            "question": self.question
        }
    
    @staticmethod
    def create() -> str:
        return '''
            CREATE TABLE IF NOT EXISTS "QOTD" (
                "question" TEXT NOT NULL
            )
        '''

    @staticmethod
    def select_row_with_id(_id: str) -> str:
        return f'''
            SELECT *
            FROM "WARNS"
            WHERE rowid='{_id}'
        '''
    
    @staticmethod
    def dict_from_tuple(query_res) -> QOTDInfo:
        return {
            "id": query_res[0],
            "question": query_res[1]
        }