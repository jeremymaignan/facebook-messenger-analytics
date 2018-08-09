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
        for row in tqdm(senders):
            #print(row)
            self.db.insert_sender(row[0], row[1], row[2], row[3], row[4], row[5])
        print("[INFO] Senders table filled")