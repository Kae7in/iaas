from flask import render_template, request, abort, redirect, url_for, jsonify
from . import site_blueprint
from iaas import models, db, login_manager
from iaas.dev import views as dev
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
import requests


class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])


class JoinForm(Form):
	username = StringField('username', validators=[DataRequired()])
	email = StringField('email', validators=[Email(), DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	password_confirm = StringField('password_confirm', validators=[DataRequired()])


class NewIntegerForm(Form):
	integer = IntegerField('value', validators=[DataRequired()])
	label = StringField('label', validators=[DataRequired()])


@site_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm(csrf_enabled=False)
	next_url = request.args.get('next')

	if current_user.is_authenticated:
		return redirect(next_url or url_for('site.dashboard'))

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
			return redirect(next_url or url_for('site.dashboard'))

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
	next_url = request.args.get('next')

	if current_user.is_authenticated:
		return redirect(next_url or url_for('site.dashboard'))

	if form.validate_on_submit():
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		password_confirm = request.form['password_confirm']

		# TODO: May not need this
		if username is None\
				or email is None\
				or password is None\
				or password_confirm is None:
			return render_template('join.html')  # TODO: Add proper response

		if password != password_confirm:
			return render_template('join.html')  # TODO: Add proper response

		# Check for prior existence of username and email
		if db.session.query(db.exists().where(models.User.username == username)).scalar()\
				or db.session.query(db.exists().where(models.User.email == email)).scalar():
			return render_template('join.html')  # TODO: Add proper response

		# Create new user object
		new_user = models.User(username=username, email=email, password=password)

		# Login user and commit to database before redirecting (order is important here)
		new_user.authenticated = True
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user, remember=True)

		return redirect(next_url or url_for('site.dashboard'))

	return render_template('join.html')


@site_blueprint.route('/')
def home():
	next_url = request.args.get('next')

	if current_user.is_authenticated:
		return redirect(next_url or url_for('site.dashboard'))
	else:
		return render_template('index.html')


@site_blueprint.route('/dashboard')
@login_required
def dashboard():
	form = NewIntegerForm(csrf_enabled=False)
	return render_template('dashboard.html', form=form)


@site_blueprint.route('/dashboard/get_all_integers', methods=['GET'])
@login_required
def get_all_integers():
	r = requests.get(url_for('dev.integerlistcontroller'),
					 headers={'Authorization': 'Token ' + current_user.api_key})

	return jsonify({
		'data': r.json()
	})


@site_blueprint.route('/dashboard/new_integer', methods=['POST'])
@login_required
def new_integer():
	next_url = request.args.get('next')

	# form = NewIntegerForm(csrf_enabled=False)

	# if form.validate_on_submit():  # TODO: Get this to freaking work
	value = request.form['value']
	label = request.form['label']

	if value is not None:
		try:
			int(value)
		except ValueError:
			redirect(url_for('site.dashboard'))
	else:
		return redirect(url_for('site.dashboard'))

	data = {
		'value': value,
		'label': label
	}

	requests.post(url_for('dev.integerlistcontroller'),
					 headers={'Authorization': 'Token ' + current_user.api_key},
					 data=data)

	return redirect(next_url or url_for('site.dashboard'))


@site_blueprint.route('/dashboard/delete_integer/<string:int_id>', methods=['POST', 'DELETE'])
@login_required
def delete_integer(int_id):
	next_url = request.args.get('next')

	if int_id is None:
		return redirect(url_for('site.dashboard'))

	requests.delete(url_for('dev.integercontroller', int_id=str(int_id)),
					 headers={'Authorization': 'Token ' + current_user.api_key})

	return '', 204



@site_blueprint.route('/docs')
def docs():
	return render_template('docs.html')


@site_blueprint.route('/new_api_key')
@login_required
def new_api_key():
	return dev.new_api_key()


@site_blueprint.route('/current_api_key')
@login_required
def current_api_key():
	return dev.current_api_key()



@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.query.get(user_id)
	except:
		return None
