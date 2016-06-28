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


class JoinForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	password_confirm = StringField('password_confirm', validators=[DataRequired()])


@site_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm(csrf_enabled=False)
	if form.validate_on_submit():
		# Get fields from form submission
		username = request.form['username']
		password = request.form['password']

		if username is None or password is None:
			return render_template('login.html')

		# Get supposed user object from database
		user = models.User.query.filter(models.User.username == username).first()

		# Verify credentials
		if user is not None and user.verify_password(password):
			# Login user and commit to database before redirecting (order is important here)
			user.authenticated = True
			db.session.add(user)
			db.session.commit()
			login_user(user, remember=True)

			# Redirect
			next_url = request.args.get('next')
			return redirect(next_url or url_for('site.home'))

	return render_template('login.html')


@site_blueprint.route('/logout')
@login_required
def logout():
	# Logout user and commit to database (order is important here)
	current_user.authenticated = False
	db.session.add(current_user)
	db.session.commit()
	logout_user()

	return redirect(url_for('site.home'))


@site_blueprint.route('/join', methods = ['GET', 'POST'])
def join():
	form = JoinForm(csrf_enabled=False)
	if form.validate_on_submit():
		username = request.form['username']
		password = request.form['password']
		password_confirm = request.form['password_confirm']

		if username is None or password is None or password_confirm is None:
			return render_template('join.html')

		if password != password_confirm:
			return render_template('join.html')

		# Create new user object
		new_user = models.User(username=username, password=password)

		# Login user and commit to database before redirecting (order is important here)
		new_user.authenticated = True
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user, remember=True)

		next_url = request.args.get('next')

		return redirect(next_url or url_for('site.home'))

	return render_template('join.html')


@site_blueprint.route('/')
def home():
	return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.query.get(user_id)
	except:
		return None