from datetime import datetime
import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

from run_aggregation import get_matching_auction_items

DEBUG = True

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results/')
def results():
    if 'username' not in request.args:
        return redirect(url_for('index'))  # redirect to index if username is not present

    context = {
        'username': request.args.get('username')
    }

    try:
        context.update(results=get_matching_auction_items(context['username']))
    except Exception:
        context.update(results={'count': 0, 'games': []})

    return render_template('results.html', context=context)


if __name__ == '__main__':
    app.run(port=8000)
