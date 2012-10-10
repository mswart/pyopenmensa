# -*- coding: utf-8 -*-
class Field(object):
	convertFunc = lambda v: v

	def __init__(self, name = None, default = None, null=True):
		self.name = name
		self.default = default
		self.null = null

	def init(self, name):
		self.name = self.name or name

	def fromJsonDict(self, jsonDict):
		value = jsonDict.get(self.name, self.default)
		if value is None and self.null:
			return value
		return self.convertFunc(value)


class StringField(Field):
	convertFunc = str

class IntegerField(Field):
	convertFunc = int

class FloatField(Field):
	convertFunc = float

class DateTimeField(Field):
	convertFunc = lambda v: datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
