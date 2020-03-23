from datetime import datetime

from flask import request

from apis.base import Base
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.utils import get_conf
from utils.logger import log
from utils.registry import registry
from models import db
from dateutil.parser import parse

class ConversationApi(Base):
    name = "conversation"

    def get_dates(self, conversations):
        return {
            "first_message": min([x[2] for x in conversations]).strftime("%b %d %Y %H:%M:%S"),
            "last_message": max([x[1] for x in conversations]).strftime("%b %d %Y %H:%M:%S")
        }

    def get(self, conversation_id=None):
        if not conversation_id:
            output = []
            conversations = db.execute_sql("select distinct title as t, count(*) as c, max(is_still_participant) from message group by t order by c desc;").fetchall()
            for conversation in conversations:
                if conversation[0] == "":
                    continue
                output.append({
                    "title": conversation[0],
                    "nb_messages": conversation[1],
                    "is_still_participant": conversation[2]
                })
        else:
            output = {
                "nb_messages_per_user": [],
                "title": conversation_id,
                "messages_per_hour": []
            }
            conversations = db.execute_sql("select count(*), max(sent_at), min(sent_at), sender, max(is_still_participant) from message where title='{}' group by sender;".format(conversation_id)).fetchall()
            output["nb_messages"] = sum([x[0] for x in conversations])
            for i, conversation in enumerate(conversations):
                output["nb_messages_per_user"].append({
                    "user": conversation[3],
                    "nb_message": conversation[0],
                    "label": conversation[3],
                    "color": get_conf("colors")[i],
                    "rate": round(conversation[0] * 100 / output["nb_messages"], 2)
                })
                output["is_still_participant"] = bool(conversation[4])
            output["nb_messages_per_user"] = sorted(output["nb_messages_per_user"], key = lambda i: i['nb_message'], reverse=True)
            output.update(self.get_dates(conversations))
            output["message_per_day"] = round(output["nb_messages"] / (parse(output["last_message"]) - parse(output["first_message"])).days, 2)

            # Add array with nb_message per hour
            messages_per_hour = db.execute_sql("select hour(sent_at) as h, count(*) from message where title='{}' group by h order by h;".format(conversation_id)).fetchall()
            for message in messages_per_hour:
                output["messages_per_hour"].append({
                    "x": "{}h".format(message[0]),
                    "y": message[1]
                })
        return messages.message(output, namespace=self.get_namespace(request))

registry.register((ConversationApi, "get_one_conversation", "/conversation/<string:conversation_id>", "GET"))
registry.register((ConversationApi, "get_conversations", "/conversation", "GET"))
