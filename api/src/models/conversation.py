import peewee

from models.base import Base, BaseEnum


class Conversation(Base):
    conversation_id = peewee.CharField()
    title = peewee.CharField()
    is_still_participant = peewee.BooleanField(default=False)
    count_messages = peewee.IntegerField()
