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

    def get_list_of_conversations(self):
        query = """
           SELECT * FROM conversations
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as err:
            print("[ERROR] Cannot fetch conversations. Error: {}".format(err))
            return []

    def __del__(self):
        self.conn.close()
