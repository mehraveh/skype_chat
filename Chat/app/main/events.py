import random, string

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . models import *

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ':'+'has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    length = random.randint(10,25)
    pm_id  = randomword(length)
    pm = SkypePmModel(pm_id=pm_id, sender=session.get('name'), text= message['msg'])
    pm.save()
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


