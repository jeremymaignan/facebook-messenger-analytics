from datetime import datetime

from flask import request

from apis.base import Base
from models.call import Call
from schemas.call import CallSchema
from utils import messages
from utils.utils import get_conf
from utils.logger import log
from utils.registry import registry
from models import db
from dateutil.parser import parse
from collections import defaultdict

def format_duration(duration_sec):
    m, s = divmod(duration_sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return "{} Days {} Hours {} Minutes {} Secondes".format(d, h, m, s)
    elif h:
        return "{} Hours {} Minutes {} Secondes".format(h, m, s)
    elif m:
        return "{} Minutes {} Secondes".format(m, s)
    return "{} Secondes".format(s)
def format_participants(participants, nb_call):
    output = []
    for name, value  in participants.items():
        output.append({
            "name": name,
            "nb_call": value["nb_call"],
            "rate": round(value["nb_call"] * 100 / nb_call, 2)
        })
    return sorted(output, key = lambda i: i['nb_call'], reverse=True)

class CallApi(Base):
    name = "call"

    def get(self, conversation_id=None):
        calls = db.execute_sql("select * from `call` where conversation_id='{}';".format(conversation_id)).fetchall()
        output = {
            "total_duration_sec": 0,
            "nb_call": 0,
            "nb_call_missed": 0,
            "participants": "",
            "total_duration_pretty": "",
            "average_duration_pretty": "",
            "average_duration_sec": ""
        }
        if not calls:
            return messages.message(output, namespace=self.get_namespace(request))
        participants = {}
        for call in calls:
            output["total_duration_sec"] += call[8]
            if call[9] == 1:
                output["nb_call_missed"] += 1
            else:
                output["nb_call"] += 1
                if call[1] not in participants:
                    participants[call[1]] = {
                        "nb_call": 0
                    }
                participants[call[1]]["nb_call"] += 1
        output["total_duration_pretty"] = format_duration(output["total_duration_sec"])
        output["average_duration_sec"] = int(output["total_duration_sec"] / output["nb_call"])
        output["average_duration_pretty"] = format_duration(output["average_duration_sec"])
        output["participants"] = format_participants(participants, output["nb_call"])
        return messages.message(output, namespace=self.get_namespace(request))

registry.register((CallApi, "get_calls", "/conversation/<string:conversation_id>/call/", "GET"))
