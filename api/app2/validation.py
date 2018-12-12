import werkzeug

from flask_restful import reqparse

req_parser = reqparse.RequestParser()
req_parser.add_argument(
        'username', type=str, required=True)

req_parser.add_argument(
        'password', type=str, required=True)