
import peewee

from utils.utils import get_conf

creds = get_conf("mysql_creds")
creds["host"] = creds["host"][get_conf("env")]
db = peewee.MySQLDatabase(**creds)
