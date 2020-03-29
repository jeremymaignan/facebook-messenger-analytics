from marshmallow import fields, validate
from models.message import ThreadType

from schemas.base import Base

class CallSchema(Base):
    id = fields.Int(required=False)
    caller = fields.Str(required=True)
    started_at = fields.DateTime(required=True)
    content = fields.Str(required=False, allow_none=True)
    conversation_id = fields.Str()
    is_still_participant = fields.Boolean()
    participants = fields.Str()
    thread_type = fields.Str(validate=validate.OneOf(choices=ThreadType.values()))
    duration = fields.Int()
    is_missed = fields.Boolean(required=False, allow_none=True)
