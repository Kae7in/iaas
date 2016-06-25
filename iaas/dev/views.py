# from flask import render_template
from flask_restful import abort, reqparse, Resource
from . import dev, dev_blueprint
from iaas import models, db, login_manager


parser = reqparse.RequestParser()
parser.add_argument('value', type=int)
parser.add_argument('label')


class IntegerController(Resource):
	def get(self, int_id):
		integer = models.Integer.query.filter(models.Integer.id == int_id).first()

		if integer is not None:
			return integer.json()
		else:
			abort(404, message="Integer {} does not exist.".format(int_id))

	def delete(self, int_id):
		integer = models.Integer.query.filter(models.Integer.id == int_id)

		if integer is not None:
			integer.delete()
			db.commit()
			return '', 204
		else:
			abort(404, message="Integer {} does not exist.".format(int_id))

	def put(self, int_id):
		args = parser.parse_args()
		integer = models.Integer.query.filter(models.Integer.id == int_id).first()

		if integer is not None and args['value'] is not None:
			integer.value = args['value']
			db.commit()
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
			integers = models.Integer.query.filter(models.Integer.label == label)
		else:
			integers = models.Integer.query.all()

		integerList = [integer.json() for integer in integers]

		return {
			'integerList': integerList
		}

	def post(self):
		args = parser.parse_args()

		newInteger = models.Integer(args['value'], args['label'])

		db.add(newInteger)
		db.commit()

		return newInteger.json()


dev.add_resource(IntegerController, '/integers/<int_id>')
dev.add_resource(IntegerListController, '/integers')


@dev_blueprint.route('/')
def devTest():
	return 'Welcome to the IAAS API!'


@login_manager.user_loader
def load_user(user_id):
	return models.User.query.filter(models.User.id == user_id).first()
