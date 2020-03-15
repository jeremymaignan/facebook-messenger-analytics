from datetime import datetime

from flask import request

from apis.base import Base
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry


class MessageApi(Base):
    name = "message"
    schema = MessageSchema()

    def get(self):
        m = Message.select().limit(100)
        return messages.message(self.schema.dump(m, many=True), namespace=self.get_namespace(request))

registry.register((MessageApi, "get_messages", "/messages", "GET"))
