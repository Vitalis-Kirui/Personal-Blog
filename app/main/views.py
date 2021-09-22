from flask import render_template
from . import main
from ..requests import get_quote

@main.route('/', methods=["GET"])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    return render_template('index.html', quote=quote)