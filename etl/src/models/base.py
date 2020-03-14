from playhouse.signals import Model

from models import db


class Base(Model):
    class Meta:
        database = db

class BaseEnum(object):
    @classmethod
    def values(cls):
        return [v for k,v in cls.__dict__.items() if isinstance(v, (str, bytes)) and k.find('__') == -1]
