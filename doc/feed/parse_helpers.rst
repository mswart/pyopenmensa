Parse helpers
=============
.. currentmodule:: pyopenmensa.feed


Date parsing
------------

The first parameter of :meth:`.BaseBuilder.addMeal` specify the date. It should be a :obj:`datetime.date`. :meth:`.LazyBuilder.addMeal` supports also :obj:`str` as type: pyopenmensa tries to extract a date from it with :func:`extractDate`. Around the date itself can be garbage strings. The following date formats are recognized as 6th March 2013:

- **2013-03-06**, 2013-03-6, 2013-3-06, 2013-3-6
- **13-03-06**, 13-03-6, 13-3-06, 13-3-6
- **06.03.2013**, 6.03.2013, 06.3.2013, 6.3.2013
- **06.03.13**, 6.03.13, 06.3.13, 6.3.13
- **06. März 2013**, 6. März 2013
- **06. Maerz 2013**, 6. Maerz 2013
- **06. März 13**, 6. März 13
- **06. Maerz 13**, 6. Maerz 13

The white spaces and the dots in the last four formats are optional.


Prices
------

OpenMensa and pyopenmensa support also meal prices. The price can be specified for different roles. See the Documentation about `OpenMensa Feed V2`__ for all supported roles.

__ http://doc.openmensa.org/feed/v2/


Internally pyopenmensa counts in cents (integers). But strings and floats can be converted with :func:`.buildPrices`. The following numbers are recognized as 3 Euro and 9 Cents:

- "3.09 €"
- "3,09 €"
- "3.09€"
- "3,09€"
- "3.09"
- "3,09"

Also these ways:

- a dictionary with a role to prices mapping::

    buildPrices({'student': '3.64 €', 'employee': 3.84, 'other': 414})

- a iterator about prices and a iterator about roles::

    buildPrices(['3.64€', 3.84, 414], ('student', 'employee', 'role'))

- base prices and additional costs for other roles::

    buildPrices(3.64, default='student', addtional={'employee': '0.20€', 'other': 50})


will create::

    {'student': 364, 'employee': 384, 'other': 414}

The fifth and sixth parameter of :meth:`.LazyBuilder.addMeal` are passed to :func:`.buildPrices` - so there is normally no need to call it directly.


Legend helpers and notes
------------------------

For every meal a feed can specify a list of additional notes. These notes are passed to `addMeal` as fourth parameter. The name contains in many cases food additive information (e.g. with number in brackets).

The :class:`.LazyBuilder` class helps with the extraction and converting of these data:

1.

    Use :meth:`.LazyBuilder.setLegendData` to define the food additive to identifier (like numbers) mapping. It uses :func:`.buildLegend` to create the legend.

    You can pass a dictionary as parameter or a text as first.

    Additionaly also a text with a regex is accepted. The regex is used to extract this mapping from the given text. Therefore the regex needs to have two named groups `name` and `value`. Per default the regex extracts a number with a following bracket until the next number with a bracket.

2. Pass the name with food additives and other optional notes to :meth:`.LazyBuilder.addMeal`. All numbers and letters in brackets will be removed from the name and the name in the legend data is added to the notes list.

Example:

::

    canteen.setLegendData('1) Schwein a)Farbstoff')
    canteen.addMeal('2013-05-02', 'Hauptgerichte', 'Gulasch(1,a)', ['Mit Süßspeise'])
    # is equal to
    canteen.addMeal('2013-05-02', 'Hauptgerichte', 'Gulasch', ['Mit Süßspeise', 'Schwein', 'Farbstoff'])

