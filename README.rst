PyOpenMensa - use OpenMensa with Python
=======================================

|Build Status| |Latest PyPI version| |Python versions| |Development status| |Documentation|

This small python library helps you to work with
`OpenMensa <http://openmensa.org/>`__ by:

-  **support writing canteen feeds**: `The feed module <#generating-openmensa-feeds>`__ makes it very easy to generate a valid `OpenMensa Feed    V2 <http://doc.openmensa.org/feed/v2/>`__. This is in production use for the majority of canteens in `OpenMensa <http://openmensa.org/>`__.
-  **python wrapper for OpenMensa data**: Access data (canteens, meals) transparent from `openmensa <http://openmensa.org/>`__. **(in development)**

More information about `OpenMensa and all possibilities for developers <http://doc.openmensa.org/>`__.


Documentation
-------------

|Documentation|

Documentation is hosted by `ReadTheDocs <https://readthedocs.org>`__: for the `Full documentation about PyOpenMensa <https://pyopenmensa.readthedocs.org>`__

The documentation is created with `Spinx <http://sphinx-doc.org/>`__ and the documentation source code can be found in the doc/ directory.


Quickstart
----------

You can create a OpenMensa feed using the ``feed`` or the ``model`` approach.
``feed`` is the original, opinionated library that automates typical tasks.
``model`` gives you more control by allowing you to build the feed from components and use builders specifically when you need them.

Installation
~~~~~~~~~~~~

1. You need `Python <http://www.python.org/>`__ 2.6, 2.7 or **>=3.2**.
2. Install pyopenmensa:

   1. via pypi

      .. code:: bash

         pip install pyopenmensa

   2. via git

      .. code:: bash

         git clone git://github.com/mswart/pyopenmensa``

Feed
~~~~

3. Create Feed builder:

   .. code:: python

      # import LazyBuilder - the container for all meals
      from pyopenmensa.feed import LazyBuilder
      canteen = LazyBuilder() # canteen container

4. Add feed data (PyOpenMensa can do basic parsing and converting):

   .. code:: python

      from datetime import date
      canteen.addMeal(date(2013, 3, 4), 'Hauptgericht', 'Gulasch',
          notes=['Mit Süßstoff', 'Schwein'],
          prices={'student': 203, 'other': '3,05 €'}
      )
      canteen.setDayClosed('5.3.2013')

5. Generate XML feed:

   .. code:: python

      print(canteen.toXMLFeed())

   And you have a valid `OpenMensa V2 Feed <http://doc.openmensa.org/feed/v2/>`__:

   .. code:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <openmensa version="2.0" xmlns="http://openmensa.org/open-mensa-v2"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" si:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">
        <canteen>
          <day date="2013-03-04">
            <category name="Hauptgericht">
              <meal>
                <name>Gulasch</name>
                <note>Mit Süßstoff</note>
                <note>Schwein</note>
                <price role="other">3.05</price>
                <price role="student">2.03</price>
              </meal>
            </category>
          </day>
          <day date="2013-03-05">
            <closed/>
          </day>
        </canteen>
      </openmensa>

Model
~~~~~

3. Build the model:

    .. code:: python

        from pyopenmensa.model import Meal, Prices, Notes, Category, Day, Canteen

        meal = Meal('Gulasch', prices=Prices(others=305, students=203), notes=Notes(['Mit Süßstoff', 'Schwein']))
        category = Category('Hauptgericht', meals=[meal])
        day = Day(datetime.date(2013, 03, 04), categories=[category])
        canteen = Canteen(days=[day])

4. Generate XML feed:

    .. code:: python

        print(canteen.to_string())

Alternatively, you can use one of the builders in ``pyopenmensa.model.builders`` to handle a common task for you.

-  ``PricesBuilder`` is used when meals share supplements for certain roles.
Instead of manually calculating the prices, ``PricesBuilder`` allows you to set the supplements once and the generate the prices for the different roles based on a default price.

-  ``NotesBuilder`` maps note keys to the full notes using a legend dict.

-  ``PricesCategoryBuilder`` will let you specify the price for an entire category and replace all the contained meals' prices with it.


Contributing
------------

1. Fork it.
2. Create a branch (``git checkout -b my_markup``)
3. Commit your changes (``git commit -am "Added Snarkdown"``)
4. Push to the branch (``git push origin my_markup``)
5. Open a `Pull Request <https://github.com/mswart/pyopenmensa/pulls>`__
6. Enjoy a refreshing Diet Coke and wait


License
-------

LGPL License

Copyright (c) 2012-2015 Malte Swart. LGPL license, see LICENSE for more
details.

.. |Build Status| image:: https://travis-ci.org/mswart/pyopenmensa.png?branch=master
    :target: https://travis-ci.org/mswart/pyopenmensa
    :alt: Build Status

.. |Latest PyPI version| image:: https://img.shields.io/pypi/v/pyopenmensa.svg
    :target: https://pypi.python.org/pypi/pyopenmensa
    :alt: Latest PyPI version

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/pyopenmensa.svg
    :target: https://pypi.python.org/pypi/pyopenmensa
    :alt: Supported Python Versions

.. |Development status| image:: https://img.shields.io/pypi/status/pyopenmensa.svg
    :target: https://pypi.python.org/pypi/pyopenmensa
    :alt: Development status

.. |Documentation| image:: https://readthedocs.org/projects/pyopenmensa/badge/?version=latest
    :target: https://pyopenmensa.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation
