PyOpenMensa - use OpenMensa with Python
=======================================

|Build Status| |Latest PyPI version|

This small python library helps you to work with
`OpenMensa <http://openmensa.org/>`__ by:

-  **support writing canteen feeds**: `The feed module <#generating-openmensa-feeds>`__ makes it very easy to generate a valid `OpenMensa Feed    V2 <http://doc.openmensa.org/feed/v2/>`__. This is in production use for the majority of canteens in `OpenMensa <http://openmensa.org/>`__.
-  **python wrapper for OpenMensa data**: Access data (canteens, meals) transparent from `openmensa <http://openmensa.org/>`__. **(in development)**

More information about `OpenMensa and all possibilities for developers <http://doc.openmensa.org/>`__.

Documentation
-------------

**See http://pyom.devtation.de/ for the `Full documentation about PyOpenMensa <http://pyom.devtation.de/>`__ **

The documentation is created with `Spinx <http://sphinx-doc.org/>`__ and the documentation source code can be found in the doc/ directory.

tldr: Documentation
-------------------

1. You need `Python <http://www.python.org/>`__ 2.6, 2.7 or **>=3.2**.
2. Install pyopenmensa:

   1. via pypi

      .. code:: bash

         pip install pyopenmensa

   2. via git

      .. code:: bash

         git clone git://github.com/mswart/pyopenmensa``

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

5. Receive XML Feed:

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

Copyright (c) 2012-2014 Malte Swart. LGPL license, see LICENSE for more
details.

.. |Build Status| image:: https://travis-ci.org/mswart/pyopenmensa.png?branch=master
    :target: https://travis-ci.org/mswart/pyopenmensa
    :alt: Build Status

.. |Latest PyPI version| image:: https://badge.fury.io/py/pyopenmensa.png
    :target: https://badge.fury.io/py/pyopenmensa
    :alt: Latest PyPI version
