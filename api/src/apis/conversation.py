from datetime import datetime

from flask import request

from apis.base import Base
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry
from models import db

class ConversationApi(Base):
    name = "conversation"

    def get(self):
        conversations = db.execute_sql("select distinct title as t, count(*) as c from message group by t order by c desc;").fetchall()
        output = []
        for conversation in conversations:
            output.append({
                "title": conversation[0],
                "nb_messages": conversation[1]
            })
        return messages.message(output, namespace=self.get_namespace(request))

registry.register((ConversationApi, "get_conversation", "/conversation", "GET"))
