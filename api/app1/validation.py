import werkzeug

from flask_restful import reqparse

req_parser = reqparse.RequestParser()
req_parser.add_argument(
        'temp', type=str, required=True)