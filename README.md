# PyOpenMensa - use OpenMensa with Python

[![Build Status](https://travis-ci.org/mswart/pyopenmensa.png?branch=master)](https://travis-ci.org/mswart/pyopenmensa)

This small python library helps you to work with [OpenMensa][om] by:

* **support writing canteen feeds**: [The feed module](#generating-openmensa-feeds) makes it very easy to generate a valid [OpenMensa Feed V2][feed_v2]
* **python wrapper for OpenMensa data**: Access data (canteens, meals) transparent from [openmensa][om]. **(in development)**

More information about [OpenMensa and all possibilities for developers][om-doc].


## Documentation

**See http://pyom.devtation.de/ for the [Full documentation about PyOpenMensa][pyom-doc]**

The documentation is created with [Spinx][sphinx] and the documentation source code can be found in the doc/ directory.

## tldr: Documentation

1.   You need [Python][python] 2.6, 2.7 or **>=3.2**.
2.   Install pyopenmensa via git:

     ```bash
     git clone git://github.com/mswart/pyopenmensa
     ```

3.   Create Feed builder:

     ```python
     # import LazyCanteen - the container for all meals
     from pyopenmensa.feed import LazyCanteen
     canteen = LazyCanteen() # canteen container
     ```

4.   Add feed data (PyOpenMensa can do basic parsing and converting):

     ```python
     from datetime import date
     canteen.addMeal(date(2013, 3, 4), 'Hauptgericht', 'Gulasch',
         notes=['Mit Süßstoff', 'Schwein'],
         prices={'student': 203, 'other': '3,05 €'}
     )
     canteen.setDayClosed('5.3.2013')
     ```

5.   Receive XML Feed:

     ```python
     print(canteen.toXMLFeed())
     ```

     And you a valid [OpenMensa V2 Feed][feed_v2]:

     ```xml
     <?xml version="1.0" encoding="UTF-8"?>
     <openmensa version="2.0" xmlns="http://openmensa.org/open-mensa-v2"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">
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
     ```


## Contributing

1. Fork it.
2. Create a branch (`git checkout -b my_markup`)
3. Commit your changes (`git commit -am "Added Snarkdown"`)
4. Push to the branch (`git push origin my_markup`)
5. Open a [Pull Request][PR]
6. Enjoy a refreshing Diet Coke and wait



[om]: http://openmensa.org/
[om-doc]:  http://doc.openmensa.org/
[pyom-doc]: http://pyom.devtation.de/
[feed_v2]: http://doc.openmensa.org/feed/v2/
[sphinx]: http://sphinx-doc.org/
[python]: http://www.python.org/
[PR]: https://github.com/mswart/pyopenmensa/pulls
