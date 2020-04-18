import peewee
from backoff import expo, on_exception

from utils.utils import get_conf

creds = get_conf("mysql_creds")
creds["host"] = creds["host"][get_conf("env")]
db = peewee.MySQLDatabase(**creds)


@on_exception(expo, peewee.OperationalError, max_tries=8)
def create_connection():
    try:
        db.connection()
    except peewee.OperationalError:
        db.connect(reuse_if_open=True)


@on_exception(expo, peewee.OperationalError, max_tries=8)
def destroy_connection(exc):
    if not db.is_closed():
        db.close()


def init(app):
    app.before_request(create_connection)
    app.teardown_request(destroy_connection)
