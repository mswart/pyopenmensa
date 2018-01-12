# -*- coding: UTF-8 -*-
from collections import namedtuple
import datetime
import re
from xml.dom.minidom import Document

try:
    from collections import OrderedDict
except ImportError:  # support python 2.6
    OrderedDict = dict


# Helpers to extract dates from strings
# -------------------------------------

date_format = re.compile(".*?(?P<datestr>(" +
                         "\d{2}(\d{2})?-[01]?\d-[0-3]?\d|" +
                         "[0-3]?\d\.[01]?\d\.\d{2}(\d{2})?|" +
                         "(?P<day>[0-3]?\d)\.? ?(?P<month>\S+) ?" +
                         "(?P<year>\d{2}(\d{2})?))).*",
                         re.UNICODE)
month_names = {
    'januar': '01',
    'january': '01',
    'februar': '02',
    'february': '02',
    'märz': '03',
    'maerz': '03',
    'march': '03',
    'april': '04',
    'mai': '05',
    'may': '05',
    'juni': '06',
    'june': '06',
    'juli': '07',
    'july': '07',
    'august': '08',
    'september': '09',
    'oktober': '10',
    'october': '10',
    'november': '11',
    'dezember': '12',
    'december': '12',
}


def extractDate(text):
    """ Tries to extract a date from a given :obj:`str`.

        :param str text: Input date. A :obj:`datetime.date` object is passed
             thought without modification.
        :rtype: :obj:`datetime.date`"""
    if type(text) is datetime.date:
        return text
    match = date_format.search(text.lower())
    if not match:
        raise ValueError('unsupported date format: {0}'.format(text.lower()))
    # convert DD.MM.YYYY into YYYY-MM-DD
    if match.group('month'):
        if not match.group('month') in month_names:
            raise ValueError('unknown month names: "{0}"'
                             .format(match.group('month')))
        year = int(match.group('year'))
        return datetime.date(
            year if year > 2000 else 2000 + year,
            int(month_names[match.group('month')]),
            int(match.group('day')))
    else:
        parts = list(map(lambda v: int(v), '-'.join(reversed(
            match.group('datestr').split('.'))).split('-')))
        if parts[0] < 2000:
            parts[0] += 2000
        return datetime.date(*parts)


class extractWeekDates():
    weekdays = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
        'Mon': 0,
        'Montag': 0,
        'Dienstag': 1,
        'Mittwoch': 2,
        'Donnerstag': 3,
        'Freitag': 4,
        'Samstag': 5,
        'Sonntag': 6
    }

    def __init__(self, start, end=None):
        self.monday = extractDate(start)

    def __getitem__(self, value):
        if type(value) not in [int, str]:
            raise TypeError
        if value not in self.weekdays:
            raise ValueError
        return self.monday + datetime.date.resolution * self.weekdays[value]

    def __iter__(self):
        for i in range(7):
            yield self.monday + datetime.date.resolution * i


# Helpers for price handling
# -------------------------------------

#: The default compiled regex that is used by :func:`.convertPrice` and
#: :func:`.buildPrices`
default_price_regex = re.compile(r'(^|[^\d,.])(?P<euro>\d+)[,.]' +
                                 r'(?P<cent>\d{2}|\d{1}(?=\s*€))',
                                 re.UNICODE)
short_price_regex = re.compile(r'[^\d]*(?P<euro>\d+)\s*€[^\d]*', re.UNICODE)
none_price_regex = re.compile(r'^\s*-\s*$', re.UNICODE)


def convertPrice(variant, regex=None, short_regex=None, none_regex=none_price_regex):
    ''' Helper function to convert the given input price into integers (cents
        count). :obj:`int`, :obj:`float` and :obj:`str` are supported

        :param variant: Price
        :param re.compile regex: Regex to convert str into price. The re should
             contain two named groups `euro` and `cent`
        :param re.compile short_regex: Short regex version (no cent part)
             group `euro` should contain a valid integer.
        :param re.compile none_regex: Regex to detect that no value is provided
             if the input data is str, the normal regex do not match and this
             regex matches `None` is returned.
        :rtype: int/None'''
    if isinstance(variant, int) and not isinstance(variant, bool):
        return variant
    elif isinstance(variant, float):
        return round(variant * 100)
    elif isinstance(variant, str):
        match = (regex or default_price_regex).search(variant) \
            or (short_regex or short_price_regex).match(variant)
        if not match:
            if none_regex and none_regex.match(variant):
                return None
            raise ValueError('Could not extract price: {0}'.format(variant))
        return int(match.group('euro')) * 100 + \
            int(match.groupdict().get('cent', '').ljust(2, '0'))
    else:
        raise TypeError('Unknown price type: {0!r}'.format(variant))


def buildPrices(data, roles=None, regex=default_price_regex,
                default=None, additional={}):
    ''' Create a dictionary with price information. Multiple ways are
        supported.

        :rtype: :obj:`dict`: keys are role as str, values are the prices as
             cent count'''
    if isinstance(data, dict):
        data = [(item[0], convertPrice(item[1])) for item in data.items()]
        return dict([v for v in data if v[1] is not None])
    elif isinstance(data, (str, float, int)) and not isinstance(data, bool):
        if default is None:
            raise ValueError('You have to call setAdditionalCharges '
                             'before it is possible to pass a string as price')
        basePrice = convertPrice(data)
        if basePrice is None:
            return {}
        prices = {default: basePrice}
        for role in additional:
            extraCharge = convertPrice(additional[role])
            if extraCharge is None:
                continue
            prices[role] = basePrice + extraCharge
        return prices
    elif roles:
        prices = {}
        priceRoles = iter(roles)
        for priceData in data:
            price = convertPrice(priceData)
            if price is None:
                continue
            prices[next(priceRoles)] = price
        return prices
    else:
        raise TypeError('This type is for prices not supported!')


# Helpers for notes and legend handling
# -------------------------------------

#: Default regex str for :func:`buildLegend`
default_legend_regex = '(?P<name>(\d|[a-z])+)\)\s*' + \
                       '(?P<value>\w+((\s+\w+)*[^0-9)]))'
#: Default compiled regex for :func:`extractNotes`
default_extra_regex = re.compile('\((?P<extra>[0-9a-zA-Z]{1,2}'
                                 '(?:,[0-9a-zA-Z]{1,2})*)\)', re.UNICODE)


def buildLegend(legend=None, text=None, regex=None, key=lambda v: v):
    ''' Helper method to build or extend a legend from a text. The given regex
        will be used to find legend inside the text.

        :param dict legend: Initial legend data
        :param str text: Text from which should legend information extracted.
            None means do no extraction.
        :param str regex: Regex to find legend part inside the given text. The
            regex should have a named group `name` (key) and a named group
            `value` (value).
        :param callable key: function to map the key to a legend key
        :rtype: dict'''
    if legend is None:
        legend = {}
    if text is not None:
        for match in re.finditer(regex or default_legend_regex,
                                 text, re.UNICODE):
            legend[key(match.group('name'))] = match.group('value').strip()
    return legend


def extractNotes(name, notes, legend=None, regex=None, key=lambda v: v):
    ''' This functions uses legend data to extract e.g. (1) references in a
        meal name and add these in full text to the notes.

        :param str name: The meal name
        :param list notes: The initial list of notes for this meal
        :param dict legend: The legend data. Use `None` to skip extraction. The
            key is searched inside the meal name (with the given regex) and if
            found the value is added to the notes list.
        :param re.compile regex: The regex to find legend references in the
            meal name. The regex must have exactly one group which identifies
            the key in the legend data. If you pass None the
            :py:data:`default_extra_regex` is used. Only compiled regex are
            supported.
        :param callable key: function to map the key to a legend key
        :rtype: tuple with name and notes'''
    if legend is None:
        return name, notes
    if regex is None:
        regex = default_extra_regex
    # extract note
    for note in list(','.join(regex.findall(name)).split(',')):
        if not note:
            continue
        note = key(note)
        if note in legend:
            if legend[note] not in notes:
                notes.append(legend[note])
        else:
            print('could not find extra note "{0}"'.format(note))
    # from notes from name
    name = regex.sub('', name).replace('\xa0', ' ').replace('  ', ' ').strip()
    return name, notes


class Feed(namedtuple('FeedRecord', ['name', 'priority', 'url', 'source', 'dayOfWeek', 'dayOfMonth', 'hour', 'minute', 'retry'])):
    def toTag(self, output):
        ''' This methods returns all data of this feed as feed xml tag

        :param output: XML Document to which the data should be added
        :type output: xml.dom.DOMImplementation.createDocument
        '''
        feed = output.createElement('feed')
        feed.setAttribute('name', self.name)
        feed.setAttribute('priority', str(self.priority))

        # schedule
        schedule = output.createElement('schedule')
        schedule.setAttribute('dayOfMonth', self.dayOfMonth)
        schedule.setAttribute('dayOfWeek', self.dayOfWeek)
        schedule.setAttribute('hour', self.hour)
        schedule.setAttribute('minute', self.minute)
        if self.retry:
            schedule.setAttribute('retry', self.retry)
        feed.appendChild(schedule)

        # url
        url = output.createElement('url')
        url.appendChild(output.createTextNode(self.url))
        feed.appendChild(url)

        # source
        if self.source:
            source = output.createElement('source')
            source.appendChild(output.createTextNode(self.source))
            feed.appendChild(source)
        return feed


# Base canteen with meal data
# ---------------------------


class BaseBuilder(object):
    """ This class represents and stores all information
        about OpenMensa canteens. It helps writing new
        python parsers with helper and shortcuts methods.
        So the complete object can be converted to a valid
        OpenMensa v2 xml feed string. """
    allowed_price_roles = ['pupil', 'student', 'employee', 'other']

    def __init__(self, version=None):
        self._days = {}
        self._version = version
        self._name = None
        self._address = None
        self._city = None
        self._phone = None
        self._email = None
        self._location = None
        self._availability = None
        self.feeds = []

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    def location(self, longitude, latitude):
        self._location = (longitude, latitude)

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, availability):
        self._availability = availability

    def define(self, **kwargs):
        self.feeds.append(Feed(**kwargs))

    def addMeal(self, date, category, name, notes=None, prices=None):
        """ This is the main helper, it adds a meal to the
            canteen. The following data are needed:

            :param datetime.date date: Date for the meal
            :param str category:  Name of the meal category
            :param str meal: Meal name.

            :raises ValueError: if the meal name is empty or longer that 250 characters
            :raises ValueError: if the price role is unknown
            :raises ValueError: if the category name is empty
            :raises ValueError: if note list contains empty note
            :raises TypeError: if the price value is not an integer

            Additional the following data are also supported:

            :param notes: List of notes
            :type notes: list
            :param prices: Price of the meal; Every key must be a string for
                 the role of the persons who can use this tariff; The value is
                 the price in Euro Cents, The site of the OpenMensa project
                 offers more detailed information.
            :type prices: dict"""
        # check name:
        if not len(name):
            raise ValueError('Meal names must not be empty')
        if len(name) > 250:
            raise ValueError('Meal names must be shorter than 251 characters')
        # check category:
        if not len(category):
            raise ValueError('Category names must not be empty')
        # process notes
        if notes:
            for note in notes:
                if not len(note):
                    raise ValueError('Note must not be empty. Left it out, if not needed')
        # process prices:
        if prices is None:
            prices = {}
        else:
            for role in prices:
                if role not in self.allowed_price_roles:
                    raise ValueError('Unknown price role "%s"' % role)
                if not isinstance(prices[role], int):
                    raise TypeError('Unsupport price type - expect integer')
        # ensure we have an entry for this date
        date = self._handleDate(date)
        if date not in self._days:
            self._days[date] = OrderedDict()
        # ensure we have a category element for this category
        if category not in self._days[date]:
            self._days[date][category] = []
        # add meal into category:
        self._days[date][category].append((name, notes or [], prices))

    def setDayClosed(self, date):
        """ Define that the canteen is closed on this date. If a day is closed,
            all stored meals for this day will be removed.

            :param date: Date of the day
            :type date: datetime.date"""
        self._days[self._handleDate(date)] = False

    def clearDay(self, date):
        """ Remove all stored information about this date (meals or closed
            information).

            :param date: Date of the day
            :type date: datetime.date"""
        date = self._handleDate(date)
        if date in self._days:
            del self._days[date]

    def dayCount(self):
        """ Return the number of dates for which information are stored.

            :rtype: int"""
        return len(self._days)

    def hasMealsFor(self, date):
        """ Checks whether for this day are information stored.

            :param date: Date of the day
            :type date: datetime.date
            :rtype: bool"""
        date = self._handleDate(date)
        if date not in self._days or self._days[date] is False:
            return False
        return len(self._days[date]) > 0

    @staticmethod
    def _handleDate(date):
        """ Internal method that is used to handle/convert input date. It
            raises a :exc:`ValueError` if the type is no
            :class:`datetime.date`. This method should be overwritten in
            subclasses to support other date input types.

            :param date: input to be handled/converted
            :rtype: datetime.date"""
        if type(date) is not datetime.date:
            raise TypeError('Dates needs to be specified by datetime.date')
        return date

    # methods to create feed
    # ----------------------

    def toXML(self):
        feed, document = self._createDocument()

        if self.version is not None:
            feed.appendChild(self._buildStringTag('version', self.version, document))

        feed.appendChild(self.toTag(document))

        return feed

    def toXMLFeed(self):
        """ Convert this cateen information into string
            which is a valid OpenMensa v2 xml feed

            :rtype: str"""
        feed = self.toXML()

        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        return xml_header + feed.toprettyxml(indent='  ')

    @staticmethod
    def _createDocument():
        # create xml document
        output = Document()
        # build main openmensa element with correct xml namespaces
        openmensa = output.createElement('openmensa')
        openmensa.setAttribute('version', '2.1')
        openmensa.setAttribute('xmlns', 'http://openmensa.org/open-mensa-v2')
        openmensa.setAttribute('xmlns:xsi',
                               'http://www.w3.org/2001/XMLSchema-instance')
        openmensa.setAttribute('xsi:schemaLocation',
                               'http://openmensa.org/open-mensa-v2 ' +
                               'http://openmensa.org/open-mensa-v2.xsd')

        return openmensa, output

    def toTag(self, output):
        ''' This methods adds all data of this canteen as canteen xml tag
        to the given xml Document.

        :meth:`toXMLFeed` uses this method to create the XML Feed. So there is
        normally no need to call it directly.

        :param output: XML Document to which the data should be added
        :type output: xml.dom.DOMImplementation.createDocument
        '''
        # create canteen tag, which represents our data
        canteen = output.createElement('canteen')
        if self._name is not None:
            canteen.appendChild(self._buildStringTag('name', self._name, output))
        if self._address is not None:
            canteen.appendChild(self._buildStringTag('address', self._address, output))
        if self._city is not None:
            canteen.appendChild(self._buildStringTag('city', self._city, output))
        if self._phone is not None:
            canteen.appendChild(self._buildStringTag('phone', self._phone, output))
        if self._email is not None:
            canteen.appendChild(self._buildStringTag('email', self._email, output))
        if self._location is not None:
            canteen.appendChild(self._buildLocationTag(self._location, output))
        if self._availability is not None:
            canteen.appendChild(self._buildStringTag('availability', self._availability, output))
        # iterate above all feeds:
        for feed in sorted(self.feeds, key=lambda v: v.priority):
            canteen.appendChild(feed.toTag(output))
        # iterate above all days (sorted):
        for date in sorted(self._days.keys()):
            day = output.createElement('day')
            day.setAttribute('date', str(date))
            if self._days[date] is False:  # canteen closed
                closed = output.createElement('closed')
                day.appendChild(closed)
                canteen.appendChild(day)
                continue
            # canteen is open
            for categoryname in self._days[date]:
                day.appendChild(self._buildCategoryTag(
                    categoryname, self._days[date][categoryname], output))
            canteen.appendChild(day)
        return canteen

    @classmethod
    def _buildStringTag(cls, tag_name, value, output):
        tag = output.createElement(tag_name)
        tag.appendChild(output.createTextNode(value))
        return tag

    @classmethod
    def _buildLocationTag(cls, location, output):
        tag = output.createElement('location')
        tag.setAttribute('longitude', location[0])
        tag.setAttribute('latitude', location[1])
        return tag

    @classmethod
    def _buildCategoryTag(cls, name, data, output):
        # skip empty categories:
        if len(data) < 1:
            return None
        category = output.createElement('category')
        category.setAttribute('name', name)
        for meal in data:
            category.appendChild(cls._buildMealTag(meal, output))
        return category

    @staticmethod
    def _buildMealTag(mealData, output):
        name, notes, prices = mealData
        meal = output.createElement('meal')
        # add name
        nametag = output.createElement('name')
        nametag.appendChild(output.createTextNode(name))
        meal.appendChild(nametag)
        # add notes:
        for note in sorted(notes):
            notetag = output.createElement('note')
            notetag.appendChild(output.createTextNode(note))
            meal.appendChild(notetag)
        # add prices:
        for role in sorted(prices):
            price = output.createElement('price')
            price.setAttribute('role', role)
            price.appendChild(output.createTextNode("{euros}.{cents:0>2}"
                              .format(euros=prices[role] // 100,
                                      cents=prices[role] % 100)))
            meal.appendChild(price)
        return meal


# Lazy version with auto extraction and convertion functions
# ----------------------------------------------------------


class LazyBuilder(BaseBuilder):
    """ An extended builder class which uses a set of helper and
        auto-converting functions to reduce common converting tasks

        :ivar extra_regex: None: regex to be passed to extractNotes, Use `None`
            to use default regex provided by this module.
        """

    def __init__(self, *args, **kwargs):
        super(LazyBuilder, self).__init__(*args, **kwargs)
        self.legendData = None
        #: function passed as key parameter to :py:func:`.buildLegend` and
        #: :py:func:`.extractNotes`; use `lambda v: v.lower()` for
        #: case-insensitive legend names (instance member)
        self.legendKeyFunc = lambda v: v
        self.extra_regex = None
        self.additionalCharges = (None, {})

    def setLegendData(self, *args, **kwargs):
        """ Set or genernate the legend data from this canteen.
            Uses :py:func:`.buildLegend` for genernating """
        self.legendData = buildLegend(*args, key=self.legendKeyFunc, **kwargs)

    def setAdditionalCharges(self, default, additional):
        """ This is a helper function, which fast up the calculation
            of prices. It is useable if the canteen has fixed
            additional charges for special roles.

            :param str default: specifies for which price role the price of
                addMeal are.
            :param dict additional: Defines the extra costs (value) for other
                roles (key)."""
        self.additionalCharges = (default, buildPrices(additional))

    def addMeal(self, date, category, name, notes=None, prices=None,
                roles=None):
        """ Same as :py:meth:`.BaseBuilder.addMeal` but uses
            helper functions to convert input parameters into needed types.
            Meals names are auto-shortend to the allowed 250 characters.
            The following paramer is new:

            :param roles:  Is passed as role parameter to :func:`buildPrices`
            """
        if self.legendData:  # do legend extraction
            name, notes = extractNotes(name, notes or [],
                                       legend=self.legendData,
                                       key=self.legendKeyFunc,
                                       regex=self.extra_regex)
        prices = buildPrices(prices or {}, roles,
                             default=self.additionalCharges[0],
                             additional=self.additionalCharges[1])
        if len(name) > 250:
            name = name[:247] + '...'
        super(LazyBuilder, self).addMeal(extractDate(date), category, name,
                                         notes or [], prices)

    @staticmethod
    def _handleDate(date):
        return extractDate(date)

OpenMensaCanteen = LazyBuilder
