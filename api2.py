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
	def find(limit=None, ids=None, near=None):
		recvCanteens = lambda **kwargs: list(map(lambda c: Canteen(values=c),
			Canteen().request('canteens', params=kwargs)))
		params = {}
		if limit:
			params['limit'] = limit
		if ids:
			params['ids'] = ','.join(map(lambda i: str(i), ids))
		if near is not None:
			params.update({ 'near[lat]': near[0], 'near[lng]': near[1] })
			if len(near) > 2:
				params['near[dist]'] = near[2]
		return recvCanteens(**params)

	def __str__(self):
		return 'Canteen({id}: {name})'.format(**self.__dict__)


class Meal(Api2Entity):
	pass
