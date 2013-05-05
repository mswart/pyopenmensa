# PyOpenMensa - use OpenMensa with Python

[![Build Status](https://travis-ci.org/mswart/pyopenmensa.png?branch=master)](https://travis-ci.org/mswart/pyopenmensa)

This small python library helps you to work with [OpenMensa][om] by:

* **support writing canteen feeds**: [The feed module](#generating-openmensa-feeds) makes it very easy to generate a valid [OpenMensa Feed V2][feed_v2]
* **python wrapper for OpenMensa data**: Access data (canteens, meals) transparent from [openmensa][om]. **(in development)**

More information about [OpenMensa and all possibilities for developers][om-doc].



## Requirements

* **Python >= 3.2**, Python 2.7 looks like it works, but the library is currently only tested with Python 3.2

No additional packages or libraries are needed.



## Generating OpenMensa Feeds


### Principle usage

The way to generate a feed is very easy:

1. Create a canteen object
2. Add meal informations to canteen
3. Receive built XML

This little example:

```python
# import OpenMensaCanteen - the container for all meals
from pyopenmensa.feed import OpenMensaCanteen
canteen = OpenMensaCanteen() # canteen container
# add meals
canteen.addMeal('2013-05-02', 'Hauptgerichte', 'Gulasch',
	[ 'Mit Süßspeise', 'Schwein', 'Farbstoff' ],
	{ 'student': '5.35' })
# create xml feed
feed = canteen.toXMLFeed()
```

creates the following XML, which can be easily parsed and processed by [OpenMensa][om]:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<openmensa version="2.0" xmlns="http://openmensa.org/open-mensa-v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">
  <canteen>
    <day date="2013-05-02">
      <category name="Hauptgerichte">
        <meal>
          <name>Gulasch</name>
          <note>Mit Süßspeise</note>
          <note>Schwein</note>
          <note>Farbstoff</note>
          <price role="student">5.35</price>
        </meal>
      </category>
    </day>
  </canteen>
</openmensa>
```


### addMeal

The important method is `canteen.addMeal(date, category, name, notes=[], prices={}, priceRoles=None)`. The parameters are described inside the next sections.

pyopenmensa preserves the ordering of adding the date into the feed in the scope of every day.


### Dates

There are some helper methods to work with dates itself:

- `setDayClosed(date)`: Define that the canteen is closed on this date. All in the previous paragraph [described date formats][date-formats] are supported. If a day is closed, all stored meals for this day will be removed.
- `clearDay(date)`: Remove all stored information about this date (meals or closed information). Again [all formats][date-formats] are supported.
- `dayCount()`: Return the number of dates for which information are stored.


[date-formats]: #date-parsing
[om]: http://openmensa.org
[om-doc]:  http://doc.openmensa.org
[feed_v2]: http://doc.openmensa.org/feed/v2/
[py-date]: http://docs.python.org/3/library/datetime.html#date-objects
