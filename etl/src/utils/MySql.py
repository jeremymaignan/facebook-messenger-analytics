import mysql.connector 
from utils.conf_manager import get_conf

class MySql():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=get_conf("mysql_host"), 
                user=get_conf("mysql_user"), 
                password=get_conf("mysql_password"), 
                database=get_conf("mysql_database"), 
                charset='utf8mb4', 
                use_unicode=True
            )
            self.cursor = self.conn.cursor()
            print("[INFO] Connected to the database {}".format(get_conf("mysql_database")))
        except Exception as err:
            print("[ERROR] Cannot connect to the Database. {}".format(err))

    def save_message(self, message, uuid):
        try:
            query = 'INSERT INTO messages(sender, sent_at, content, gifs, photos, share, sticker, video, type, title, is_still_participant, participants, thread_type, thread_path, uuid) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            values = (
                message.sender,
                message.sent_at,
                message.content,
                message.gifs,
                message.photos,
                message.share,
                message.sticker,
                message.video,
                message.type,
                message.title,
                message.is_still_participant,
                message.participants,
                message.thread_type,
                message.thread_path,
                uuid
            )
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as err:
            print("[ERROR] Cannot insert message in Database. {}".format(err))
            #print(message)

    def messages_by_sender_by_conversation(self):
        query = """
        SELECT title, uuid, sender, COUNT(*), MIN(sent_at), MAX(sent_at) FROM messages
        GROUP BY title, uuid, sender;
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as err:
            print("[_PROSPECTOR_] [ERROR] Cannot fetch messages_by_sender_by_conversation. Error: {}".format(err))

    def insert_sender(self, title, uuid, sender, nb_messages_sent, first_message_sent_at, last_message_sent_at):
        query = """
            insert into senders(username, conversation_id, first_message_sent_at, last_message_sent_at, nb_messages_sent)
            values(
                "{}",
                (SELECT id FROM conversations WHERE title = "{}" and uuid = "{}"),
                "{}",
                "{}",
                {}
            );
        """.format(sender, title, uuid, first_message_sent_at, last_message_sent_at, nb_messages_sent)
        #print(query)
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as err:
            print(title)
            print("[ERROR] Cannot insert sender. Error: {}".format(err))

    def messages_by_conversation(self):
        query = """
           INSERT INTO conversations (title, participants, nb_messages, created_at, last_message_sent_at, is_still_participant, uuid)
                SELECT title, 
                    participants, 
                    count(*),
                    MIN(sent_at),
                    MAX(sent_at),
                    is_still_participant,
                    uuid
                FROM messages
                GROUP BY title, participants, uuid, is_still_participant;
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as err:
            print("[ERROR] Cannot fill conversation table. Error: {}".format(err))

    def __del__(self):
        self.conn.close()
