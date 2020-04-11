from datetime import datetime

from dateutil.parser import parse
from flask import request

from apis.base import Base
from models import db
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry
from utils.utils import get_conf
import langid
from collections import defaultdict
import pycountry

class ConversationApi(Base):
    name = "conversation"

    def get_dates(self, conversations):
        return {
            "first_message": min([x[2] for x in conversations]).strftime("%b %d %Y %H:%M:%S"),
            "last_message": max([x[1] for x in conversations]).strftime("%b %d %Y %H:%M:%S")
        }

    def get_language(self, conversation_id):
        """
            Keep only message with > 20 char and 5 words
            Get language of each messages
            Keep 4 most used languages
            Add others value's = sum of all others languages
        """
        message_per_lang = defaultdict(int)
        messages_ = db.execute_sql("""
            SELECT content
            FROM message
            WHERE 
                conversation_id='{}' AND
                content IS NOT NULL AND
                content <> "" AND
                CHARACTER_LENGTH(content) > 20
            """.format(conversation_id)).fetchall()
        log.info("{} messages found".format(len(messages_)))
        messages_ = [x[0] for x in messages_ if len(x[0].split(' ')) >= 5]
        log.info("{} messages with words".format(len(messages_)))
        for content in messages_:
            try:
                content = content.encode('latin1', 'ignore').decode('utf8')
            except:
                continue
            lang = langid.classify(content)[0]
            message_per_lang[lang] += 1
        output = []
        for lang, nb in message_per_lang.items():
            output.append({
                "lang": lang,
                "language_pretty": pycountry.languages.get(alpha_2=lang).name,
                "nb_messages": nb,
                "flag": get_conf("flags").get(lang, get_conf("flags").get("other"))
            })
        output = sorted(output, key = lambda i: i['nb_messages'], reverse=True)
        others = sum([x["nb_messages"] for x in output[4:]])
        output = output[:4]
        output.append({
            "lang": "others",
            "language_pretty": "Others",
            "nb_messages": others,
            "flag": get_conf("flags")["other"]
        })
        return messages.message(output, namespace=self.get_namespace(request))

    def get_conversation_info(self, conversation_id):
        output = {
            "nb_messages_per_user": [],
            "messages_per_hour": []
        }
        conversations = db.execute_sql("""
            SELECT
                COUNT(*),
                MAX(sent_at),
                MIN(sent_at),
                sender,
                ANY_VALUE(is_still_participant),
                ANY_VALUE(title),
                ANY_VALUE(thread_type)
            FROM message
            WHERE conversation_id='{}'
            GROUP BY sender;
            """.format(conversation_id)).fetchall()
        
        output["nb_messages"] = sum([x[0] for x in conversations])
        for i, conversation in enumerate(conversations):
            output["title"] = conversation[5]
            output["is_group_conversation"] = True if conversation[6] == "RegularGroup" else False
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
        try:
            output["message_per_day"] = round(output["nb_messages"] / (parse(output["last_message"]) - parse(output["first_message"])).days, 2)
        except ZeroDivisionError:
            output["message_per_day"] = 0.0
        return messages.message(output, namespace=self.get_namespace(request))

    def get_conversation_list(self, conversation_id):
        output = []
        conversations = db.execute_sql("""
        SELECT
            DISTINCT title AS t,
            COUNT(*) as c,
            ANY_VALUE(is_still_participant),
            ANY_VALUE(conversation_id)
        FROM message GROUP BY t
        ORDER BY c DESC;
        """).fetchall()
        for conversation in conversations:
            if conversation[0] == "":
                continue
            output.append({
                "title": conversation[0],
                "nb_messages": conversation[1],
                "is_still_participant": conversation[2],
                "conversation_id": conversation[3]
            })
        return messages.message(output, namespace=self.get_namespace(request))

    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "info":
            return self.get_conversation_info(conversation_id)
        elif data_to_get == "conversation_list":
            return self.get_conversation_list(conversation_id)
        elif data_to_get == "languages":
            return self.get_language(conversation_id)

registry.register((ConversationApi, "get_one_conversation", "/conversation/<string:conversation_id>", "GET"))
registry.register((ConversationApi, "get_conversations", "/conversation", "GET"))
