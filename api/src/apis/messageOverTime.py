from flask import request

from apis.base import Base
from models import db
from schemas.message import MessageSchema
from utils import messages
from utils.logger import log
from utils.registry import registry
from utils.utils import get_conf


class MessageOverTimeApi(Base):
    name = "message_over_time"
    schema = MessageSchema()

    def get_messages_per_day(self, conversation_id):
        messages_per_day = db.execute_sql("""
        SELECT 
            DAYOFWEEK(sent_at) AS d,
            sender,
            COUNT(*)
        FROM message
        WHERE conversation_id='{}'
        GROUP BY d, sender;
        """.format(conversation_id)).fetchall()

        # Load in dict
        messages_per_day_per_user = {}
        for message in messages_per_day:
            if message[1] not in messages_per_day_per_user:
                messages_per_day_per_user[message[1]] = {
                    "color": get_conf("colors")[len(messages_per_day_per_user)],
                    "data": []
                }
            messages_per_day_per_user[message[1]]["data"].append({
                "x": get_conf("days_of_week")[int(message[0])],
                "y": message[2]
            })

        # Build output
        output = []
        for name, value in messages_per_day_per_user.items():
            # Put sunday at the end of the list
            value["data"] = value["data"][1:] + [value["data"][0]]
            value.update({"title": name})
            output.append(value)
        return messages.message(output, namespace=self.get_namespace(request))

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

    def get_messages_per_month(self, conversation_id):
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

    def get(self, conversation_id=None):
        data_to_get = request.args.get('data')
        if data_to_get == "hour":
            return self.get_messages_per_hour(conversation_id)
        elif data_to_get == "day":
            return self.get_messages_per_day(conversation_id)
        elif data_to_get == "month":
            return self.get_messages_per_month(conversation_id)
        return messages.bad_request("Not Found")

registry.register((MessageOverTimeApi, "get_messages_over_time", "/conversation/<string:conversation_id>/messages_over_time", "GET"))
