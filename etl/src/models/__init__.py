import peewee

from utils.utils import get_conf

db = peewee.MySQLDatabase(**get_conf("mysql_creds"))
