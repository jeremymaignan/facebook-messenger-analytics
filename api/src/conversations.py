import json
from flask import Flask, Response, Blueprint
from utils.MySql import MySql
import ast

get_conversations_list_route = Blueprint('get_conversations', __name__)
get_one_conversation_route = Blueprint('get_one_conversation', __name__)
get_messages_per_hour_route = Blueprint('get_messages_per_hour', __name__)
get_users_route = Blueprint('get_users', __name__)

@get_conversations_list_route.route("/conversations",  methods=['GET'])
def get_conversations():
    db = MySql()
    response = []
    conversations = db.get_list_of_conversations()
    if [] == conversations:
        return Response(
            status=500,
            mimetype='application/json'
        )
    for row in conversations:
        response.append({
            "id": row['id'],
            "title": row['title'],
            "nb_messages": row['nb_messages'],
            "participant": ast.literal_eval(row['participants']),
            "created_at": row['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            "is_group_conversation": False if 1 == len(ast.literal_eval(row['participants'])) else True
        })
    return Response(
        response=json.dumps({"conversations": response}),
        status=201,
        mimetype='application/json'
    )

@get_messages_per_hour_route.route("/messages_per_hours",  methods=['GET'])
def get_messages_per_hour():
    db = MySql()
    messages = db.get_nb_messages_per_hour()
    if [] == messages:
        return Response(
            status=500,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({"messages": messages}),
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

@get_users_route.route("/users",  methods=['GET'])
def get_users():
    db = MySql()
    users = db.get_users()
    if [] == users:
        return Response(
            status=500,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({"users": users}),
        status=201,
        mimetype='application/json'
    )
