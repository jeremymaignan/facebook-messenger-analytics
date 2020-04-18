from collections import defaultdict
from datetime import datetime

from dateutil.parser import parse
from flask import request

from apis.base import Base
from models import db
from models.message import Message
from models.conversation import Conversation
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry
from utils.utils import decode_str, get_conf


class ConversationList(Base):
    name = "conversation_list"

    def get(self, conversation_id=None):
        output = []
        for conversation in Conversation.select().order_by(Conversation.count_messages.desc()):
            if conversation.title == "":
                continue
            output.append({
                "title": conversation.title,
                "nb_messages": str(conversation.count_messages),
                "is_still_participant": conversation.is_still_participant,
                "conversation_id": conversation.conversation_id
            })
        return messages.message(output, namespace=self.get_namespace(request))

registry.register((ConversationList, "get_conversations", "/conversation", "GET"))
