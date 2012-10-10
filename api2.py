# -*- coding: UTF-8 -*-
from .wrapper import Entity
from .fields import *

class Api2Entity(Entity):
	default_api_base = 'http://openmensa.org/api/v2/'

class Canteen(Api2Entity):
	name = StringField()
	address = StringField()
	latitude = FloatField()
	longitude = FloatField()

	def __init__(self, id=None):
		super(Canteen, self).__init__()
		if id:
			self.fromJsonDict(self.request('canteens/{id}'.format(id=int(id))))
		else:
			self.fromJsonDict({})


class Meal(Api2Entity):
	pass
