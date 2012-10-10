# -*- coding: UTF-8 -*-
from urllib.request import urlopen, build_opener
from urllib.parse import urljoin, urlparse, urlunparse, urlencode
import re
import json

from fields import *


class Entity(object, metaclass=ModelMeta):
	default_api_base = 'http://openmensa.org/api/v2/'
	default_opener = build_opener()
	charset_pattern = re.compile('.*charset=(?P<encoding>[\w-]+)')

	def __init__(self, api_base=None, opener=None):
		self.api_base = api_base or self.default_api_base
		self.opener = opener or self.default_opener

	def fromJsonDict(self, jsonDict):
		for name in self._fields:
			setattr(self, name, self._fields[name].fromJsonDict(jsonDict))

	def request(self, name, params={}):
		# build url with api_base, name + params
		response = self.opener.open(urlunparse(
			list(urlparse(urljoin(self.api_base, name))[0:4]) +
			[ urlencode(params), None ]
		))
		# read content, decode to string if possible
		contentType = response.headers['Content-Type'] or ''
		charsettest = self.charset_pattern.match(contentType)
		if charsettest:
			content = response.readall().decode(charsettest.group('encoding'))
		else:
			content = response.readall()
		# parse content-type
		if contentType.startswith('application/json'):
			content = json.loads(content)
		# store response object for advanced usage
		self.response = response
		return content


class Canteen(Entity):
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


class Meal(Entity):
	pass
