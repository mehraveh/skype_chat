# -*- coding: utf-8 -*-
import os

from flask import g, abort, request, session
from flask_restful import Resource, marshal

from .setting import *
from .util import *
from .model import *
from .validation import *

from ..models import *
from ..settings import *


class TestResource(Resource):

    url = 'ter'

    def get(self):
        args = req_parser.parse_args()
        return "GET %s" % args["temp"]

    def post(self):
        args = req_parser.parse_args()
        return "POST %s" % args["temp"]


class Test2Resource(Resource):

    url = 'ter'

    def get(self):
        args = req_parser.parse_args()
        return "GET %s" % args["temp"]

    def post(self):
        args = req_parser.parse_args()
        return "POST %s" % args["temp"]