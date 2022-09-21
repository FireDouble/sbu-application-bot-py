import time

from typing import TypedDict

from utils.schemas.SchemaAbstract import Schema

class WarnedMemberInfo(TypedDict):
    member: int
    reason: str
    moderator: int
    time: int

class WarnedMember(Schema):
    
    DB_NAME = 'warns'

    def __init__(self, member: int, guild: int, reason: str, moderator: int, time: int, warn_id: int):
        self.member = member
        self.guild = guild
        self.reason = reason
        self.moderator = moderator
        self.time = time
        self.id = warn_id
    
    def insert(self) -> (str, dict):
        
        return '''
            INSERT
            INTO WARNS
            VALUES (:member, :guild, :reason, :moderator, :time, :id)
        ''', {
            "member": self.member,
            "guild": self.guild,
            "reason": self.reason,
            "moderator": self.moderator,
            "time": self.time,
            "id": self.id
        }
    
    @staticmethod
    def create() -> str:
        return '''
            CREATE TABLE IF NOT EXISTS "WARNS" (
                "member" TEXT NOT NULL,
                "guild" INTEGER NOT NULL,
                "reason" TEXT DEFAULT 'None',
                "moderator" TEXT NOT NULL,
                "time" TEXT NOT NULL,
                "id" INTEGER NOT NULL
            )
        '''

    @staticmethod
    def select_row_with_id(_id: str) -> str:
        return f'''
            SELECT *
            FROM "WARNS"
            WHERE member='{_id}'
        '''
    
    @staticmethod
    def dict_from_tuple(query_res) -> WarnedMemberInfo:
        return {
            "member": query_res[0],
            "guild": query_res[1],
            "reason": query_res[2],
            "moderator": query_res[3],
            "time": query_res[4],
            "id": query_res[5]
        }

