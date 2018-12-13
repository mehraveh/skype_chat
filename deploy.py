import random, string

from flask import Flask, render_template, session
from flask_sse import sse
from flask_session import Session

from api.models import *


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.secret_key = 'any random string'
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
        session['username'] = username
        return session['username'] +'$' + """
        <div id='room'>
        <br>
        Callee:<br>
        <input type="text" id="callee" >
        <br>
        <button type="submit" onclick="create()"> create room </button> 
        </div>"""


@app.route("/login1/<string:username>/<string:password>",  methods=['GET'])
def login1(username, password):
    user = SkypeUserModel.objects(username=username, password=password).first()
    if not user:
        sse.publish({"message": 'no user'}, type='loginn')
        return 'no user'
    else:
        sse.publish({"message": user.username + ' ' + user.password}, type='loginn')
        return user.username + ' ' + user.password 


@app.route("/signup/<string:username>/<string:password>",  methods=['POST'])
def signup(username, password):
    user = SkypeUserModel(username=username, password=password)
    user.save()
    return '<h1>' + user.username + ' ' + user.password + '</h1>'


@app.route("/signup1/<string:username>/<string:password>",  methods=['GET'])
def signup1(username, password):
    user = SkypeUserModel(username=username, password=password)
    user.save()
    sse.publish({"message": user.username + ' ' + user.password}, type='greeting')
    return user.username + ' ' + user.password


@app.route("/create/<string:caller>/<string:callee>",  methods=['POST'])
def create(caller, callee):
    length = random.randint(5,15)
    room_id  = randomword(length)
    caller_o = SkypeUserModel.objects(username=caller).first()
    if not caller_o:
        return 'The caller dosent exist'
    callee_o = SkypeUserModel.objects(username=callee).first()
    if not callee_o:
        return 'The callee dosent exist'
    room = SkypeRoomModel(room_id=room_id, caller=caller,  callee=callee)
    room.save()
    return session['username'] +' sent chat request to ' + callee + ' with chat id ' + room_id + '. wait for her/him to accept'


@app.route("/rooms/", methods=['POST'])
def rooms():
    callers = []
    html_code = ''
    rooms = SkypeRoomModel.objects(accepted=False, callee=session['username'])
    for room in rooms:
        callers.append(room.caller)
    for caller in callers:    
        html_code +='<a href="/join/' + session['username'] + '"/>' + caller +'</a> <br>'
    return html_code 


@app.route("/join/<string:callee>/")
def join(callee):
    room = SkypeRoomModel.objects(callee=callee).first()
    room.accepted = True
    room.save()
    print(session['username'])
    sse.publish({"message": 'joined chat'}, type= room.callee)
    return 'joined'


@app.route("/join2/")    
def join2():
    return render_template('pv.html')
            