# -*- coding: UTF-8 -*-
from .wrapper import Entity
from .fields import *

class Api2Entity(Entity):
	default_api_base = 'http://openmensa.org/api/v2/'

	def __repr__(self):
		return self._type + '(' + ','.join(map(lambda v: v + '=' + repr(getattr(self, v)), self._fields)) + ')'

class Canteen(Api2Entity):
	id = IntegerField()
	name = StringField()
	address = StringField()
	latitude = FloatField()
	longitude = FloatField()

	def __init__(self, id=None, values={}):
		super(Canteen, self).__init__()
		if id:
			self.fromJsonDict(self.request('canteens/{id}'.format(id=int(id))))
		else:
			self.fromJsonDict(values)

	@staticmethod
	def find(ids=None):
		if ids:
			ids = ','.join(map(lambda i: str(i), ids))
			cs = Canteen().request('canteens', params = { 'ids': ids })
			return list(map(lambda c: Canteen(values=c), cs))
		raise NotImplemented

	def __str__(self):
		return 'Canteen({id}: {name})'.format(**self.__dict__)


class Meal(Api2Entity):
	pass
