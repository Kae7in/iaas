from flask import jsonify
from flask_restful import abort, reqparse, Resource
from . import dev, dev_blueprint
from iaas import models, db, login_manager
from flask_login import login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


parser = reqparse.RequestParser()
parser.add_argument('value', type=int)
parser.add_argument('label')


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

		if integer is not None and args['value'] is not None:
			integer.value = args['value']
			db.session.commit()
		elif integer is not None:
			abort(404, message='Invalid parameters or key name - please use value=int')
		elif args['value'] is not None:
			abort(404, message="Integer {} does not exist.".format(int_id))
		else:
			abort(404, message='You should never get this error response, else Python is broken.')

		return integer.json(), 201


class IntegerListController(Resource):

	def get(self):
		args = parser.parse_args()
		label = args['label']

		if label is not None:
			integers = models.Integer.query.filter(models.Integer.user_id == current_user.id)\
											.filter(models.Integer.label == label)
		else:
			integers = models.Integer.query.filter(models.Integer.user_id == current_user.id)

		integerList = [integer.json() for integer in integers]

		return {
			'integerList': integerList
		}

	def post(self):
		args = parser.parse_args()

		new_integer = models.Integer(args['value'], args['label'], current_user.id)

		db.session.add(new_integer)
		db.session.commit()

		return new_integer.json()


@dev_blueprint.route('/')
def dev_home():
	return 'Welcome to the IAAS API!'


# GET API KEY
@dev_blueprint.route('/api_key')
@login_required
def get_api_key():
	# Generate token unique to current user
	token = current_user.get_auth_token()

	# Store new token on user's api_token property
	current_user.api_key = token

	# Commit user update to database
	db.session.add(current_user)
	db.session.commit()

	return jsonify({
		'key': current_user.api_key.decode('ascii')
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
		api_key = api_key.replace('Basic ', '', 1)
		try:
			api_key = unicode(api_key)
		except TypeError:
			pass
		user = models.User.query.filter_by(api_key=api_key).first()
		if user:
			return user
	# finally, return None if both methods did not login the user
	return None


@login_manager.token_loader
def load_user_from_token(token):
	# Decrypt token
	data = Serializer.load(token)

	# Find the user
	user = models.User.get(data['user_id'])

	# Check password and return user or None
	if user and data['password_hash'] == user.password_hash:
		return user
	return None


dev.add_resource(IntegerController, '/integers/<int_id>')
dev.add_resource(IntegerListController, '/integers')
dev.decorators = [login_required]
