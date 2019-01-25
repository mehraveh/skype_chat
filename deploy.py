import random, string
import webbrowser
import base64

from flask import request
from flask import Flask, render_template, session
from flask_sse import sse
from flask_session import Session
from werkzeug.datastructures import ImmutableMultiDict
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
        <button type="submit" onclick="create()" class="btn--blue"> create room </button> 
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
    callee_o = SkypeUserModel.objects(username=callee).first()
    message = ''
    if not caller_o:
        message = 'The caller dosent exist'
    elif not callee_o:
        message = 'The callee dosent exist'
    elif not callee in caller_o.contacts:
        message = 'Sorry he/she isnt in your contacts'
    else:
        message = 'new chat request from ' + room.caller + " to " + room.callee 
    room = SkypeRoomModel(room_id=room_id, caller=caller,  callee=callee)
    room.save()
    sse.publish({"message": message} , type='room', channel='r')
    return session['username'] +' sent chat request to ' + callee + ' with chat id ' + room_id + '. wait for her/him to accept' + ' $ ' + room_id


@app.route("/rooms/", methods=['POST'])
def rooms():
    callers = []
    html_code = ''
    rooms = SkypeRoomModel.objects(accepted=False, callee=session['username'])
    for room in rooms:
        callers.append(room.caller)
    for caller in callers:    
        #html_code +='<a href="/join/' + session['username'] + '/'+ room.room_id +'"/>' + caller +'</a> <br>'
        html_code += '<button type="submit" onclick="select('+ "'" + room.room_id +"'"+')"> ' + caller +' </button> <br>'
    return html_code 


@app.route("/contacts/", methods=['POST'])
def contacts():
    html_code = ''
    users = SkypeUserModel.objects()
    for user in users:
        html_code += '<p>' + user.username +'<br>'+ '<button type="submit" onclick="addc(' + "'" + user.username + "'"+ ')"> ' + 'add' +' </button>' + '</p> <br>'
    return html_code


@app.route("/add/<string:username>/<string:contact>/", methods=['POST'])
def add(username, contact):
    print(username, contact)
    user = SkypeUserModel.objects(username=username).first()
    if not contact in user.contacts:
        user.contacts.append(contact)
        user.save()
    return 'success'


@app.route("/mycontacts/<string:username>/", methods=['POST'])
def mycontacts(username):
    html_code = ''
    user = SkypeUserModel.objects(username=username).first()
    for contact in user.contacts:
        html_code += '<p>' + contact + '</p><br>'
    return html_code


@app.route("/join/<string:callee>/", methods=['POST'])
def join(callee):
    room = SkypeRoomModel.objects(callee=callee, accepted=False).first()
    room.accepted = True
    room.save()
    sse.publish({"message": 'joined chat'}, type='join', channel="s")
    return 'joined'


# @app.route("/join2/<string:user>/<string:room>/", methods=['GET'])    
# def join2(user, room):
#     # b = request.user_agent.browser
#     # if b == 'chrome':
#     #     b = 'google-chrome'
#     sse.publish({"message": 'joined chat 2'}, type='join2', channel="ss")    
#     return 'joineddd'
#     # webbrowser.get(b).open_new_tab('http://192.168.1.51:5000/'+ user + '/' + room + '/')
#     # return render_template('pv.html')

            
@app.route("/videochat1/<string:user>/", methods=['GET'])    
def videochat1(user):
    print(user)
    print('sssss')
    sse.publish({"message": 'joined video chat'}, type='joinv', channel="v")
    return 'joined'


@app.route("/videochat/<string:user>/", methods=['GET'])    
def videochat(user):
    return render_template('videochat.html', user=user)


@app.route("/videochatacpt/<string:user>/", methods=['GET'])    
def videochatacpt(user):
    return render_template('videochatacpt.html', user=user)


@app.route("/send/<channel_name>/<massage_type>", methods=['POST'])
def send(channel_name, massage_type):
    print("Hello channel send!" + ' ' + massage_type + ' ' + channel_name)
    print(request.data)
    sse.publish({"message": request.data}, type=massage_type, channel=channel_name)
    return "send"  


@app.route('/save/', methods=["POST"])
def save():
    video_stream = request.form.get('video')
    print(video_stream)
    return request.form['video']
