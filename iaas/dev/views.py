from flask import jsonify
from flask_restful import abort, reqparse, Resource
from . import dev, dev_blueprint
from iaas import models, db, login_manager
from flask_login import login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


parser = reqparse.RequestParser()
parser.add_argument('value', type=int)
parser.add_argument('label')
parser.add_argument('newValue', type=int)
parser.add_argument('newLabel')


class IntegerController(Resource):

	def get(self, int_id):
		integer = models.Integer.query.filter(models.Integer.user_id == current_user.id)\
									.filter(models.Integer.id == int_id).first()

		if integer is not None:
			return integer.json()
		else:
			abort(404, message="Integer {} does not exist.".format(int_id))

	def delete(self, int_id):
		integer = models.Integer.query.filter(models.Integer.user_id == current_user.id)\
									.filter(models.Integer.id == int_id)

		if integer is not None:
			integer.delete()
			db.session.commit()
			return '', 204
		else:
			abort(404, message="Integer {} does not exist.".format(int_id))

	def put(self, int_id):
		args = parser.parse_args()
		integer = models.Integer.query.filter(models.Integer.user_id == current_user.id)\
									.filter(models.Integer.id == int_id).first()

		if integer is None:
			abort(404, message="Integer {} does not exist.".format(int_id))

		if integer is not None and args['value'] is not None:
			integer.value = args['value']

		if integer is not None and args['label'] is not None:
			integer.label = args['label']

		db.session.commit()

		return integer.json(), 201


class IntegerListController(Resource):

	def get(self):
		args = parser.parse_args()
		label = args['label']
		value = args['value']

		integers = models.Integer.query.filter(models.Integer.user_id == current_user.id)

		if label is not None:
			integers = integers.filter(models.Integer.label == label)

		if value is not None:
			integers = integers.filter(models.Integer.value == value)

		integerList = [integer.json() for integer in integers]

		return jsonify({
			'integer_list': integerList
		})

	def post(self):
		args = parser.parse_args()

		new_integer = models.Integer(args['value'], args['label'], current_user.id)

		db.session.add(new_integer)
		db.session.commit()

		return new_integer.json()

	def delete(self):
		args = parser.parse_args()
		label = args['label']
		value = args['value']

		integers = models.Integer.query.filter(models.Integer.user_id == current_user.id)

		if label is not None:
			integers = integers.filter(models.Integer.label == label)

		if value is not None:
			integers = integers.filter(models.Integer.value == value)

		integers.delete()

		db.session.commit()

		integerList = [integer.json() for integer in integers]

		return jsonify({
			'deleted_integers': integerList
		})

		return '', 204

	def put(self):
		args = parser.parse_args()
		label = args['label']
		value = args['value']

		newLabel = args['newLabel']
		newValue = args['newValue']

		if newLabel is None and newValue is None:
			return {
				'updated_integers': []
			}

		integers = models.Integer.query.filter(models.Integer.user_id == current_user.id)

		if label is not None:
			integers = integers.filter(models.Integer.label == label)

		if value is not None:
			integers = integers.filter(models.Integer.value == value)

		updatedIntegers = []
		for integer in integers:
			if newValue:
				integer.value = newValue

			if newLabel:
				integer.label = newLabel

			updatedIntegers.append(integer.json())

		db.session.commit()

		return jsonify({
			'updated_integers': updatedIntegers
		})


@dev_blueprint.route('/')
def dev_home():
	return 'Welcome to the IAAS API!'


# GET API KEY
@dev_blueprint.route('/new_api_key')
@login_required
def new_api_key():
	# Generate token unique to current user
	token = current_user.get_auth_token()

	# Store new token on user's api_token property
	current_user.api_key = token

	# Commit user update to database
	db.session.add(current_user)
	db.session.commit()

	return jsonify({
		'api_key': current_user.api_key.decode('ascii')
	})


@dev_blueprint.route('/current_api_key')
@login_required
def current_api_key():
	if current_user.api_key is None:
		current_user.api_key = current_user.get_auth_token()

		db.session.add(current_user)
		db.session.commit()

	return jsonify({
		'api_key': current_user.api_key.decode('ascii')
	})


# VERIFY API KEY
@login_manager.request_loader
def load_user_from_request(request):
	# First, try to login using the api_key url arg
	api_key = request.args.get('api_key')

	if api_key:
		user = models.User.query.filter_by(api_key=api_key).first()
		if user:
			return user

	# Next, try to login using Basic Auth
	api_key = request.headers.get('Authorization')
	if api_key:
		api_key = api_key.replace('Token ', '', 1)
		try:
			api_key = unicode(api_key)
		except TypeError:
			pass
		user = models.User.query.filter_by(api_key=api_key).first()
		if user:
			return user
	# finally, return None if both methods did not login the user
	return None


# TODO: User token for loading user instead of user id
# @login_manager.token_loader
# def load_user_from_token(token):
# 	serializer = Serializer(app.secret_key, expires_in=None)
#
# 	# Decrypt token
# 	data = serializer.load(token)
#
# 	# Find the user
# 	user = models.User.get(data['user_id'])
#
# 	# Check password and return user or None
# 	if user and data['password_hash'] == user.password_hash:
# 		return user
# 	return None


dev.add_resource(IntegerController, '/integers/<int_id>')
dev.add_resource(IntegerListController, '/integers')
dev.decorators = [login_required]
