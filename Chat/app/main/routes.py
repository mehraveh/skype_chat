from flask import session, redirect, url_for, render_template, request
from . import main


@main.route('/<string:user>/<string:room_id>/', methods=['GET', 'POST'])
def index(user, room_id):
    room_id = 1
    session['name'] = user
    session['room'] = room_id
    return redirect(url_for('.chat'))


@main.route('/chat/')
def chat():
    return render_template('chat.html', name=session['name'], room=session['room'])
