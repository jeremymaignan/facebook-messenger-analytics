from marshmallow import fields, validate

from models.message import MessageType, ThreadType
from schemas.base import Base


class MessageSchema(Base):
    id = fields.Int(required=False)
    sender = fields.Str(required=True)
    sent_at = fields.DateTime(required=True)
    content = fields.Str(required=False, allow_none=True)
    gifs = fields.Str(required=False, allow_none=True)
    photos = fields.Str(required=False, allow_none=True)
    share = fields.Str(required=False, allow_none=True)
    sticker = fields.Str(required=False, allow_none=True)
    video = fields.Str(required=False, allow_none=True)
    audio = fields.Str(required=False, allow_none=True)
    type = fields.Str(validate=validate.OneOf(choices=MessageType.values()))
    title = fields.Str()
    conversation_id = fields.Str()
    is_still_participant = fields.Boolean()
    participants = fields.Str()
    thread_type = fields.Str(validate=validate.OneOf(choices=ThreadType.values()))
