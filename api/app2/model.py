from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import *


class TestModel(Document):
    test = StringField()


class Test2Model(Document):
    test = StringField()