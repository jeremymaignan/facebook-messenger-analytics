import json
from flask import Flask, Response, Blueprint
from utils.MySql import MySql
import ast

get_conversations_list_route = Blueprint('get_conversations', __name__)
get_one_conversation_route   = Blueprint('get_one_conversation', __name__)


@get_conversations_list_route.route("/conversations",  methods=['GET'])
def get_conversations():
    db = MySql()
    response = {}
    conversations = db.get_list_of_conversations()
    if [] == conversations:
        return Response(
            status=500,
            mimetype='application/json'
        )
    for row in conversations:
        response[str(row[0])] = {
            "title": row[1],
            "participants": ast.literal_eval(row[2]),
            "nb_messages": row[3],
            "created_at": row[4].strftime('%Y-%m-%d %H:%M:%S')
        }
        print(response)
        response[str(row[0])]["is_group_conversation"] = False if 1 == len(response[str(row[0])]["participants"]) else True
    
    return Response(
        response=json.dumps(response),
        status=201,
        mimetype='application/json'
    )

@get_one_conversation_route.route("/conversations/<conversation_id>",  methods=['GET'])
def get_one_conversation(conversation_id):
    return Response(
        response="conv: {}".format(conversation_id),
        status=201,
        mimetype='application/json'
    )