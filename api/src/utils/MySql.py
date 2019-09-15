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
            self.cursor = self.conn.cursor(dictionary=True)
            print("[INFO] Connected to the database {}".format(get_conf("mysql_database")))
        except Exception as err:
            print("[ERROR] Cannot connect to the Database. {}".format(err))

    def get_list_of_conversations(self):
        query = """
        SELECT * FROM conversations ORDER BY nb_messages DESC
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as err:
            print("[ERROR] Cannot fetch conversations. Error: {}".format(err))
            return []

    def get_nb_messages_per_hour(self):
        query = """
            SELECT DATE_FORMAT(sent_at,'%H') AS hour, count(*) AS nb_messages FROM messages GROUP BY hour ORDER BY nb_messages DESC;
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as err:
            print("[ERROR] Cannot fetch messages per hour. Error: {}".format(err))
            return []

    def get_users(self):
        query = """
            select distinct username from senders order by username;
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as err:
            print("[ERROR] Cannot fetch users. Error: {}".format(err))
            return []

    def __del__(self):
        self.conn.close()
