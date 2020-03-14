import peewee

from models.base import Base, BaseEnum


class MessageType(BaseEnum):
    GENERIC = "Generic"
    SHARE = "Share"
    UNSUBSCRIBE = "Unsubscribe"
    SUBSCRIBE = "Subscribe"
    CALL = "Call"
    PLAN = "Plan"

class ThreadType(BaseEnum):
    REGULAR_GROUP = "RegularGroup"
    REGULAR = "Regular"

class Message(Base):
    sender = peewee.CharField()
    sent_at = peewee.DateTimeField(null=True, default=None)
    content = peewee.TextField(null=False, default='')
    gifs = peewee.CharField()
    photos = peewee.CharField()
    share = peewee.CharField()
    sticker = peewee.CharField()
    video = peewee.CharField()
    type = peewee.CharField()
    title = peewee.TextField(null=False, default='')
    conversation_id = peewee.CharField()
    is_still_participant = peewee.BooleanField(default=False)
    thread_type = peewee.CharField()
    participants = peewee.TextField()
