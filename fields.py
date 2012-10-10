# -*- coding: utf-8 -*-


class ModelMeta(type):
	def __new__(cls, name, bases, attrs):
		doctype = attrs.setdefault('_type', name)
		fields = {}
		for base in bases:
			baseFields = getattr(base, '_fields', {})
			for field in baseFields:
				fields[field] = copy.copy(baseFields[field])
		for elementname in list(attrs.keys()):
			element = attrs[elementname]
			if issubclass(type(element), Field):
				fields[elementname] = attrs.pop(elementname)
		attrs['_fields'] = fields
		finishedModel = type.__new__(cls, name, bases, attrs)
		for fieldname in fields:
			field = fields[fieldname]
			field._model = finishedModel
			field.init(fieldname)
		return finishedModel


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
