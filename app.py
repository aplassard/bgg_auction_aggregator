from datetime import datetime
import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

DEBUG = True

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results/')
def results():
    if 'username' not in request.args:
        return redirect(url_for('index'))  # redirect to index if username is not present
    return render_template('results.html')


if __name__ == '__main__':
    app.run(port=8000)
