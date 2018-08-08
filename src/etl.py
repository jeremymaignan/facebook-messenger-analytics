#!/usr/local/bin/python3.7
# coding: utf8

""" TODO
1. Unzip zip
2. Store reactions to messages
3. Create requirements.txt
4. Update type of sent_at in DB -> datetime
5. Remove IFs (parse_conversation())
6. Ignore chatbot, games (remove $folders_to_ignore)
"""

import os
import json
from utils.message import Messages
from utils.MySql import MySql

folders_to_ignore = ["stickers_used", '.DS_Store', "connectthedots_0fa20e74fd"]

def get_conversations_name():
    conversations_name = os.listdir('../messages')
    for folder_to_ignore in folders_to_ignore:
        if folder_to_ignore in conversations_name:
            conversations_name.remove(folder_to_ignore)
    return conversations_name

def open_conversations(filename):
    with open(filename) as content:
        return json.load(content)

def parse_conversation(conversation_json):
    messages = []
    for message in conversation_json["messages"]:
        if "content" not in message:
            message["content"] = ""
        if "gifs" not in message:
            message["gifs"] = []
        if "share" not in message:
            message["share"] = {}
        if "photos" not in message:
            message["photos"] = []
        if "sticker" not in message:
            message["sticker"] = {}
        if "videos" not in message:
            message["videos"] = []
        if "participants" not in conversation_json:
            conversation_json["participants"] = []
        if "sender_name" not in message:
            message["sender_name"] = ""
        if "title" not in conversation_json:
            conversation_json["title"] = ""     
        messages.append(Messages(
            message["sender_name"],
            message["timestamp_ms"],
            message["content"],
            message["gifs"],
            message["photos"],
            message["share"],
            message["sticker"],
            message["videos"],
            message["type"],
            conversation_json["title"],
            conversation_json["is_still_participant"],
            conversation_json["participants"],
            conversation_json["thread_type"],
            conversation_json["thread_path"]
        ))
    return messages

conversations_name = get_conversations_name()
print("[INFO] {} conversations found".format(len(conversations_name)))

db = MySql()

for conversation_name in conversations_name:
    conversation_json = open_conversations("../messages/{}/message.json".format(conversation_name))
    messages = parse_conversation(conversation_json)
    print("[INFO] {} messages in {}".format(len(messages), conversation_json["title"].encode('latin1').decode('utf8')))
    for message in messages:
        db.save_message(message)
