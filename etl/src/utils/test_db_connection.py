import time

import mysql.connector

from conf_manager import get_conf


def try_connection():
    try:
        mysql.connector.connect(
            host=get_conf("mysql_host"), 
            user=get_conf("mysql_user"), 
            password=get_conf("mysql_password"), 
            database=get_conf("mysql_database"), 
            charset='utf8mb4', 
            use_unicode=True
        )
        print("Connected")
    except Exception as err:
        print("Retry in 1 sec. err: {}".format(err))
        time.sleep(1)
        try_connection()
    
try_connection()
