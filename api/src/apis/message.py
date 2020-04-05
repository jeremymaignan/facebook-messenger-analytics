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

    def get_messages_per_hour(self, conversation_id):
        output = {
            "messages_per_hour": []
        }
        messages_per_hour = db.execute_sql("""
        SELECT
            HOUR(sent_at) AS h,
            COUNT(*)
        FROM message
        WHERE
            conversation_id='{}'
        GROUP BY h
        ORDER BY h;
        """.format(conversation_id)).fetchall()
        for message in messages_per_hour:
            output["messages_per_hour"].append({
                "x": "{}h".format(message[0]),
                "y": message[1]
            })
        return messages.message(output, namespace=self.get_namespace(request))

    def get_messages_per_months(self, conversation_id):
        output = {
            "messages_per_month": []
        }
        messages_per_month = db.execute_sql("""
        SELECT
            DATE_FORMAT(sent_at, '%%Y-%%m') AS y,
            COUNT(*)
        FROM message
            WHERE conversation_id='{}'
        GROUP BY y
        ORDER BY y ASC;
        """.format(conversation_id)).fetchall()
        for message in messages_per_month:
            output["messages_per_month"].append({
                "x": "{month}/01/{year}".format(month=message[0].split('-')[1], year=message[0].split('-')[0]),
                "y": message[1]
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


    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "message_per_hour":
            return self.get_messages_per_hour(conversation_id)
        if data_to_get == "message_per_month":
            return self.get_messages_per_months(conversation_id)
        if data_to_get == "content":
            return self.get_content(conversation_id)

registry.register((MessageApi, "get_messages", "/conversation/<string:conversation_id>/messages", "GET"))
