#!/usr/local/bin/python3.7
# coding: utf8

""" TODO
1. Unzip zip
2. Store reactions to messages
6. Ignore chatbot, games (remove $folders_to_ignore)
7. RM useless subfolder (gifs, audios, photos ...)
"""

import json
import logging
import os
import sys
from datetime import datetime

from models.call import Call
from models.message import Message
from schemas.call import CallSchema
from schemas.message import MessageSchema
from utils.logger import log
from utils.utils import decode_str, get_conf, open_file

folders_to_ignore = ["stickers_used", '.DS_Store', "connectthedots_0fa20e74fd"]

def get_conversations_names():
    conversations_name = os.listdir(get_conf("messages_files_path"))
    # Ignore folders which are not a convo
    for folder_to_ignore in folders_to_ignore:
        if folder_to_ignore in conversations_name: conversations_name.remove(folder_to_ignore)
    return conversations_name

def parse_conversation(conversation_json, conversation_name):
    schema = MessageSchema()
    messages = []
    calls = []
    for message in conversation_json["messages"]:
        participants = [decode_str(x["name"]) for x in conversation_json["participants"]]
        if  message["type"] == "Call":
            calls.append({
                "caller": decode_str(message["sender_name"]),
                "started_at": datetime.fromtimestamp(message["timestamp_ms"] / 1000.0).isoformat(),
                "content": decode_str(message.get("content", None)),
                "conversation_id": conversation_name,
                "is_still_participant": conversation_json["is_still_participant"],
                "participants": ', '.join(participants),
                "thread_type": conversation_json["thread_type"],
                "duration": message.get("call_duration", None),
                "is_missed": message.get("missed", None)
            })
        else:
            messages.append(schema.load({
                "sender": decode_str(message["sender_name"]),
                "sent_at": datetime.fromtimestamp(message["timestamp_ms"] / 1000.0).isoformat(),
                "content": message.get("content", None),
                "gifs": ', '.join([x["uri"] for x in message["gifs"]]) if "gifs" in message else None,
                "photos": ', '.join([x["uri"] for x in message["photos"]]) if "photos" in message else None,
                "share": message["share"].get("link", None) if "share" in message else None,
                "sticker": message["sticker"].get("uri", None) if "sticker" in message else None,
                "audio": message["audio_files"][0].get("uri", None) if "audio_files" in message else None,
                "video": ', '.join([x["uri"] for x in message["videos"]]) if "videos" in message else None,
                "type": message["type"],
                "title": decode_str(conversation_json["title"]),
                "conversation_id": conversation_name,
                "is_still_participant": conversation_json["is_still_participant"],
                "participants": ', '.join(participants),
                "thread_type": conversation_json["thread_type"],
            }))
    return messages, calls

def load_messages():
    # Get all conversations based on folder name
    conversations_names = get_conversations_names()
    log.info("{} conversations found".format(len(conversations_names)))

    for c, conversation_name in enumerate(conversations_names):
        path = "{}/{}/".format(get_conf("messages_files_path"), conversation_name)
        nb_file = len([name for name in os.listdir(path) if ".json" in name])
        log.info("{} files in conversation {}".format(nb_file, conversation_name))
        for i in range(1, nb_file + 1):
            log.info("Conversation: [{}/{}] File: [{}/{}]".format(c, len(conversations_names), i, nb_file))
            filename = "{}/message_{}.json".format(path, i)
            # Open json file
            conversation_json = open_file(filename)
            # Create model message and save item in db
            messages, calls = parse_conversation(conversation_json, conversation_name)
            Call.insert_many(calls).execute()
            Message.insert_many(messages).execute()

if __name__ == '__main__':
    logging.basicConfig(
        level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper()),
        format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s'
    )
    load_messages()
