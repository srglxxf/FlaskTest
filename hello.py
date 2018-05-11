from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is token'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@127.0.0.1/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
botstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False))

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

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField("Submit")

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref = 'role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #manager.run()
