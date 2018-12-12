import random, string

from flask import Flask, render_template
from flask_sse import sse

from api.models import *


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@app.route('/')
def main():
    return render_template('main.html')

@app.route("/login/<string:username>/<string:password>",  methods=['POST'])
def login(username, password):
    user = SkypeUserModel.objects(username=username, password=password).first()
    if not user:
        return None
    else:
        return user.username   


@app.route("/signup/<string:username>/<string:password>",  methods=['POST'])
def signup(username, password):
    user = SkypeUserModel(username=username, password=password)
    user.save()
    sse.publish({"message": user.username + ' ' + user.password}, type='text', channel='no ch')
    return user.username + ' ' + user.password


@app.route("/create/<string:caller>/<string:callee>")
def create_room(caller, callee):
    length = random.randint(5,15)
    room_id = 0
    while 1 :
        room_id  = randomword(length)
        room_temp = SkypeRoomModel.objects(room_id=room_id)
        if not room:
            break
    room = SkypeRoomModel(room_id=room_id)
    room.caller = caller
    room.callee = callee
    room.save()
    return room, username, 'caller'


@app.route("/join/<string:caller>/<string:room_id>")
def join_room(caller, room_id):
    room = SkypeRoomModel.objects(room_id=room_id, caller=caller)
    if not room:
        return None, 'caller'
    else:
        return room, 'callee'
            