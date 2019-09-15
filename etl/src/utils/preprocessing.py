from utils.MySql import MySql
from tqdm import tqdm

class Preprocessing():

    def __init__(self, db):
        self.db = db

    def preprocess_conversations(self):
        self.db.messages_by_conversation()
        print("[INFO] Conversations table filled")

    def preprocess_senders(self):
        senders = self.db.messages_by_sender_by_conversation()
        if [] == senders:
            return None
        for sender in tqdm(senders):
            self.db.insert_sender(sender["title"], sender["uuid"], sender["sender"], sender['nb_messages'], sender['first_message_sent_at'], sender['last_message_sent_at'])
        print("[INFO] Senders table filled")
