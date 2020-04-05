from datetime import datetime

from flask import request

from apis.base import Base
from models import db
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry


class MessageApi(Base):
    name = "message"
    schema = MessageSchema()

    def get_message_per_hour(self, conversation_id):
        output = {
            "messages_per_hour": []
        }
        messages_per_hour = db.execute_sql("select hour(sent_at) as h, count(*) from message where conversation_id='{}' group by h order by h;".format(conversation_id)).fetchall()
        for message in messages_per_hour:
            output["messages_per_hour"].append({
                "x": "{}h".format(message[0]),
                "y": message[1]
            })
        return messages.message(output, namespace=self.get_namespace(request))

    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "message_per_hour":
            return self.get_message_per_hour(conversation_id)


registry.register((MessageApi, "get_messages", "/conversation/<string:conversation_id>/messages", "GET"))
