from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


@main.route('/<string:user>/', methods=['GET', 'POST'])
def index(user):
    session['name'] = user
    session['room'] = 1
    return redirect(url_for('.chat'))


@main.route('/chat/')
def chat():
    print(session['name'])
    return render_template('chat.html', name=session['name'], room=session['room'])
