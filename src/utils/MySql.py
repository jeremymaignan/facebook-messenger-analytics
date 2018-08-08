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
            print("[INFO] Connected to the Database. {}".format(get_conf("mysql_database")))
        except Exception as err:
            print("[ERROR] Cannot connect to the Database. {}".format(err))

    def save_message(self, message):
        try:
            query = 'INSERT INTO messages(sender, sent_at, content, gifs, photos, share, sticker, video, type, title, is_still_participant, participants, thread_type, thread_path) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
                message.thread_path
            )
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as err:
            print("[ERROR] Cannot insert message in Database. {}".format(err))
            #print(message)

    def __del__(self):
        self.conn.close()
