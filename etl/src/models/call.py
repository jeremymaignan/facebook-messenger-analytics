import peewee

from models.base import Base, BaseEnum


class Call(Base):
    caller = peewee.CharField()
    started_at = peewee.DateTimeField()
    content = peewee.TextField(null=False, default='')
    conversation_id = peewee.CharField()
    is_still_participant = peewee.BooleanField(default=False)
    participants = peewee.TextField()
    thread_type = peewee.CharField()
    duration = peewee.IntegerField()
    is_missed = peewee.BooleanField(default=None)
