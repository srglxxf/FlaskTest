from flask import Flask, request, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from datetime import datetime

app = Flask(__name__)
manager = Manager(app)
botstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/time')
def get_time():
    return render_template('time.html', time=datetime.utcnow())

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    return render_template('user.html', name = username)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #manager.run()
