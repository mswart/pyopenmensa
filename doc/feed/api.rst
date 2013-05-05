Feed API
========
.. module:: pyopenmensa.feed


Base Canteen Feed Builder
-------------------------

.. autoclass:: BaseBuilder
   :members:
   :private-members: _handleDate


Lazy Canteen Feed Builder
-------------------------

.. autoclass:: LazyBuilder
   :members:

Dates
^^^^^

.. autofunction:: extractDate

Prices
^^^^^^

.. autofunction:: convertPrice

.. autofunction:: buildPrices

.. autodata:: default_price_regex

Notes and Legends
^^^^^^^^^^^^^^^^^

.. autofunction:: buildLegend

.. autodata:: default_legend_regex

.. autofunction:: extractNotes

.. autodata:: default_extra_regex
