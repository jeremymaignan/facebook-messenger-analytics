#!/usr/local/bin/python3.7
# coding: utf8

""" TODO
1. Unzip zip
2. Store reactions to messages
3. Create requirements.txt
4. Update type of sent_at in DB -> datetime
5. Remove IFs (parse_conversation())
6. Ignore chatbot, games (remove $folders_to_ignore)
7. RM useless subfolder (gifs, audios, photos ...)
"""

import os
import json
from utils.message import Messages
from utils.conf_manager import get_conf
from utils.preprocessing import Preprocessing
from utils.MySql import MySql
from tqdm import tqdm

folders_to_ignore = ["stickers_used", '.DS_Store', "connectthedots_0fa20e74fd"]
message_blank_value = {
    "content": "",
    "gifs": [],
    "share": {},
    "photos": [],
    "sticker": {},
    "videos": [],
    "sender_name": ""
}
conversation_blank_value = {
    "participants": [],
    "title": ""  
}

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

        for key in message_blank_value.keys():
            if key not in message:
                message[key] = message_blank_value[key]
        for key in conversation_blank_value.keys():
            if key not in conversation_json:
                conversation_json[key] = conversation_blank_value[key]

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

def loading(db):
    conversations_name = get_conversations_name()
    print("[INFO] {} conversations found".format(len(conversations_name)))

    for conversation_name in tqdm(conversations_name):
        conversation_json = open_conversations("../messages/{}/message.json".format(conversation_name))
        messages = parse_conversation(conversation_json)
        if len(messages) > get_conf("minimum_nb_message") and \
            len(messages) < get_conf("maximum_nb_message"):
            #print("[INFO] {} messages in {}".format(len(messages), conversation_json["title"].encode('latin1').decode('utf8')))
            for message in messages:
                db.save_message(message, conversation_name)

if __name__ == '__main__':
    db = MySql()
    preproc = Preprocessing(db)

    loading(db)
    preproc.preprocess_conversations()
    preproc.preprocess_senders()


