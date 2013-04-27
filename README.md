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


### Principiell usage

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

### Date parsing

The first parameter of `addMeal` specify the date. It should be a [python `datetime.Date` object][py-date]. If you pass a `str`, pyopenmensa tries to extract a date from it. Around the date itself can be garbage strings. The following date formats for the 6th March 2013:

 -  **2013-03-06**, 2013-03-6, 2013-3-06, 2013-3-6
 -  **13-03-06**, 13-03-6, 13-3-06, 13-3-6
 -  **06.03.2013**, 6.03.2013, 06.3.2013, 6.3.2013
 -  **06.03.13**, 6.03.13, 06.3.13, 6.3.13
 -  **06. März 2013**, 6. März 2013
 -  **06. Maerz 2013**, 6. Maerz 2013
 -  **06. März 13**, 6. März 13
 -  **06. Maerz 13**, 6. Maerz 13

The white spaces and the dots in the last four formats are optional.


### Dates

There are some helper methods to work with dates itself:

- `setDayClosed(date)`: Define that the canteen is closed on this date. All in the previous paragraph [described date formats][date-formats] are supported. If a day is closed, all stored meals for this day will be removed.
- `clearDay(date)`: Remove all stored information about this date (meals or closed information). Again [all formats][date-formats] are supported.
- `dayCount()`: Return the number of dates for which information are stored.


### Prices

OpenMensa and pyopenmensa support also meal prices. The price can be specified for different roles. See the [OpenMensa Feed V2 Documentation][feed_v2] for all supported roles.

Internally pyopenmensa counts in cents (integers). But strings and floats can be converted with `canteen.buildPrices`. The following numbers are recognized as 3 Euro and 9 Cents:

- "3.09 €"
- "3,09 €"
- "3.09€"
- "3,09€"
- "3.09"
- "3,09"

Also these ways:

- a dictionary with a role to prices mapping

  ```python
  buildPrices({'student': '3.64 €', 'employee': 3.84, 'others': 414})
  ```

- a iterator about prices and a iterator about roles.

  ```python
  buildPrices(['3.64€', 3.84, 414], ('student', 'employee', 'role'))
  ```

- base prices and additional costs for other roles:

  ```python
  buildPrices(3.64, default='student', addtional={'employee': '0.20€', 'others': 50})
  ```

will create:

```python
{'student': 364, 'employee': 384, 'others': 414}
```

The fifth and sixth parameter of `addMeal` are passed to `buildPrices` - so there is normally no need to call it directly.


### Legend helpers and notes

For every meal a feed can specify a list of additional notes. These notes are passed to `addMeal` as fourth parameter. The name contains in many cases food additive information (e.g. with number in brackets).

The `canteen` class helps with the extraction and converting of these data:

1. Use `canteen.setLegendData` to define the food additive to identifier (like numbers) mapping. You can pass a dictionary as parameter or a text as first and a regex as second parameter. If provided the regex is used to extract this mapping from the given text. Therefore the regex needs to have two named groups `name` and `value`. Per default the regex extracts a number with a following bracket until the next number with a bracket.

2. Pass the name with food additives and other optional notes to `addMeal`. All numbers and letters in brackets will be removed from the name and the name in the legend data is added to the notes list.

Example:

```python
canteen.setLegendData('1) Schwein a)Farbstoff')
canteen.addMeal('2013-05-02', 'Hauptgerichte', 'Gulasch(1,a)', ['Mit Süßspeise'])
# is equal to
canteen.addMeal('2013-05-02', 'Hauptgerichte', 'Gulasch', ['Mit Süßspeise', 'Schwein', 'Farbstoff'])
```


[date-formats]: #date-parsing
[om]: http://openmensa.org
[om-doc]:  http://doc.openmensa.org
[feed_v2]: http://doc.openmensa.org/feed/v2/
[py-date]: http://docs.python.org/3/library/datetime.html#date-objects
