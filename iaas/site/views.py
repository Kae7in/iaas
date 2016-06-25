from flask import render_template, request, abort, redirect, url_for
from . import site_blueprint
from iaas import models, db, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])


@site_blueprint.route('/users', methods = ['POST'])
def new_user():
	username = request.form['username']
	password = request.form['password']

	if username is None or password is None:
		return "Must provide username and password"
	if models.User.query.filter(models.User.username == username).first() is not None:
		return "That username is already taken."

	user = models.User(username=username)
	user.set_password(password)

	db.add(user)
	db.commit()

	return str(user.json())


@site_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm(csrf_enabled=False)
	if form.validate_on_submit():
		username = request.form['username']
		password = request.form['password']

		if username is None or password is None:
			return "Must provide both a username and password"

		user = models.User.query.filter(models.User.username == username).first()
		if user is not None and user.verify_password(password):
			user.authenticated = True
			db.session.add(user)
			db.session.commit()
			login_user(user, remember=True)
			next = request.args.get('next')
			return redirect(next or url_for('site.home'))

	return render_template('login.html')


@site_blueprint.route('/logout')
@login_required
def logout():
	current_user.authenticated = False
	db.session.add(current_user)
	db.session.commit()

	logout_user()

	return redirect(url_for('site.home'))


@site_blueprint.route('/')
def home():
	return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.query.get(user_id)
	except:
		return None