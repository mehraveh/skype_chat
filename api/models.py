from bson import ObjectId
from pymongo.errors import InvalidStringData

from mongoengine import connect, register_connection
from mongoengine.context_managers import switch_db
from mongoengine.errors import NotUniqueError
from mongoengine import (
    Document, StringField, DateTimeField, IntField, FloatField, DictField, ListField, ReferenceField,
    ListField, EmbeddedDocumentField, EmbeddedDocument, BooleanField)


connect('skype', host="127.0.01", port=27017)


class SkypeUserModel(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    contacts = ListField(StringField())


class SkypeRoomModel(Document):
    room_id = StringField(unique=True, required=True)
    caller = StringField()
    callee = StringField()
    chats = ListField(StringField())


class SkypePmModel(Document):
    pm_id = StringField(unique=True, required=True)
    sender = StringField(required=True)
