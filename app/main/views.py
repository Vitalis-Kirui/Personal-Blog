from flask import render_template,request,redirect,url_for,abort
from . import main
from ..requests import get_quote
from flask_login import login_required
from ..models import User

@main.route('/', methods=["GET"])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    return render_template('index.html', quote=quote)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)