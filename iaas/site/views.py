# from flask import render_template
from flask import request, abort
from . import site_blueprint
from iaas import models
from iaas import db


@site_blueprint.route('/users', methods = ['POST'])
def new_user():
	username = request.form['username']
	password = request.form['password']

	if username is None or password is None:
		return "Must provide username and password"
	if models.User.query.filter(models.User.username == username).first() is not None:
		return "That username is already taken."

	user = models.User(username=username)
	user.hash_password(password)

	db.add(user)
	db.commit()

	return str(user.json())


@site_blueprint.route('/')
def siteTest():
	return 'Welcome to IAAS!'
