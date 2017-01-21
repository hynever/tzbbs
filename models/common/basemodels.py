#coding: utf8
from exts import db

class BaseModel(object):

    def to_dict(self):
        return {c.name: getattr(self,c.name) for c in self.__table__.columns}