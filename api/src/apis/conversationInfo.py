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
from utils.utils import decode_str, get_conf, format_duration


class ConversationInfoApi(Base):
    name = "conversation_info"

    def get_conversation_info(self, conversation_id):
        conversations = db.execute_sql("""
            SELECT
                COUNT(*),
                MAX(sent_at),
                MIN(sent_at),
                sender,
                ANY_VALUE(is_still_participant),
                ANY_VALUE(title),
                ANY_VALUE(thread_type),
                SUM(LENGTH(content) - LENGTH(REPLACE(content, ' ', '')) + 1)
            FROM message
            WHERE conversation_id='{}'
            GROUP BY sender;
            """.format(conversation_id)).fetchall()

        # Build output
        output = {
            "nb_messages_per_user": [],
            "nb_messages": sum([x[0] for x in conversations]),
            "title": conversations[0][5],
            "is_group_conversation": True if conversations[0][6] == "RegularGroup" else False,
            "is_still_participant": bool(conversations[0][4]),
            "first_message": min([x[2] for x in conversations]).strftime("%b %d %Y %H:%M:%S"),
            "last_message": max([x[1] for x in conversations]).strftime("%b %d %Y %H:%M:%S"),
            "nb_words": sum([int(x[7]) for x in conversations]),
        }
        output["words_per_message"] = round(output["nb_words"] / output["nb_messages"], 2)
        # Calculate messages per day
        try:
            output["message_per_day"] = round(output["nb_messages"] / (parse(output["last_message"]) - parse(output["first_message"])).days, 2)
        except ZeroDivisionError:
            output["message_per_day"] = 0.0

        # Add participants, nb messages/participants, sort list
        for i, conversation in enumerate(conversations):
            output["nb_messages_per_user"].append({
                "user": conversation[3],
                "nb_message": conversation[0],
                "label": conversation[3],
                "color": get_conf("colors")[i],
                "rate": round(conversation[0] * 100 / output["nb_messages"], 2),
                "words": int(conversation[7]),
                "time_spent": format_duration(int(conversation[7]) * 1.4)
            })
        output["nb_messages_per_user"] = sorted(output["nb_messages_per_user"], key = lambda i: i['nb_message'], reverse=True)
        return messages.message(output, namespace=self.get_namespace(request))

    def get_events(self, conversation_id):
        # Get all message with type "Subscribe" or "Unsubscribe"
        messages_per_day = Message.select() \
            .where(Message.conversation_id == conversation_id) \
            .where(Message.type.in_(["Subscribe", "Unsubscribe"])) \
            .order_by(Message.sent_at.asc())

        # Format output (clean content and add change +1 or -1)
        output = []
        for message in messages_per_day:
            tmp = {
                "sent_at": message.sent_at.strftime("%b %d %Y"),
                "content": decode_str(message.content).replace(" to the group.", "").replace(" from the group.", "").replace(" the group.", ""),
                "sender": message.sender
            }
            if "added" in tmp["content"]:
                tmp["content"] = "{} added{}".format(tmp["sender"], tmp["content"].split("added")[1])
                tmp["change"] = "+1"
            elif "removed" in tmp["content"]:
                tmp["content"] = "{} removed{}".format(tmp["sender"], tmp["content"].split("removed")[1])
                tmp["change"] = "-1"
            elif "left" in tmp["content"]:
                tmp["change"] = "-1"
            output.append(tmp)
        return messages.message(output, namespace=self.get_namespace(request))

    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "info":
            return self.get_conversation_info(conversation_id)
        elif data_to_get == "events":
            return self.get_events(conversation_id)
        return messages.bad_request("Not Found")

registry.register((ConversationInfoApi, "get_one_conversation", "/conversation/<string:conversation_id>", "GET"))
