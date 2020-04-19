from collections import defaultdict

import emoji
import langid
import pycountry
from flask import request

from apis.base import Base
from models import db
from models.message import Message
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry
from utils.utils import decode_str, get_conf


class MessageApi(Base):
    name = "message"
    schema = MessageSchema()

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

        # Build output
        output = []
        for lang, nb in message_per_lang.items():
            output.append({
                "lang": lang,
                "language_pretty": pycountry.languages.get(alpha_2=lang).name,
                "nb_messages": nb,
                "flag": get_conf("flags").get(lang, get_conf("flags").get("other"))
            })
        output = sorted(output, key = lambda i: i['nb_messages'], reverse=True)
        # Merge "other" language
        others = sum([x["nb_messages"] for x in output[4:]])
        # Keep top 5
        output = output[:4]
        output.append({
            "lang": "others",
            "language_pretty": "Others",
            "nb_messages": others,
            "flag": get_conf("flags")["other"]
        })
        return messages.message(output, namespace=self.get_namespace(request))

    def get_content(self, conversation_id):
        content = db.execute_sql("""
        SELECT
            COUNT(photos),
            COUNT(video),
            COUNT(share),
            COUNT(sticker),
            COUNT(gifs),
            COUNT(audio)
        FROM message
            WHERE conversation_id='{}'
        """.format(conversation_id)).fetchall()[0]
        return messages.message({
            "photos": content[0],
            "videos": content[1],
            "shares": content[2],
            "stickers": content[3],
            "gifs": content[4],
            "audios": content[5]
        }, namespace=self.get_namespace(request))

    def get_emojies(self, conversation_id):
        nb_emojis = {}

        # Get all message with a content
        messages_ = Message.select() \
            .where(Message.content != None) \
            .where(Message.content != "") \
            .where(Message.type == "Generic") \
            .where(Message.conversation_id == conversation_id)
        log.info("{} messages found".format(len(messages_)))

        # Group emojies by users
        for message in messages_:
            try:
                tmp = message.content.encode('latin1').decode('utf8')
            except:
                continue
            for char in tmp:
                if char in emoji.UNICODE_EMOJI:
                    if message.sender not in nb_emojis:
                        nb_emojis[message.sender] = defaultdict(int)
                    nb_emojis[message.sender][char] += 1

        # Format output and keep only the top 10
        output = []
        for sender, value in nb_emojis.items():
            tmp = {
                "sender": sender,
                "emoji": []
            }
            for emoji_, count in value.items():
                tmp["emoji"].append({
                    'emoji': emoji_,
                    "nb_messages": count
                })
                tmp["emoji"] = sorted(tmp["emoji"], key = lambda i: i['nb_messages'], reverse=True)[:10]
            output.append(tmp)
        return messages.message(output, namespace=self.get_namespace(request))

    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "content":
            return self.get_content(conversation_id)
        elif data_to_get == "emojis":
            return self.get_emojies(conversation_id)
        elif data_to_get == "languages":
            return self.get_language(conversation_id)
        return messages.bad_request("Not Found")

registry.register((MessageApi, "get_messages", "/conversation/<string:conversation_id>/messages", "GET"))
