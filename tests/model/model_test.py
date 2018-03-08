import datetime
try:
    from itertools import zip_longest  # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest  # Python 2

import lxml.etree as ET
import pytest

# TODO: Use absolute paths
from ...model import Canteen, Category, ClosedDay, Day, Meal, Notes, Prices


def test_canteen_to_string():
    canteen = Canteen(days=[
        Day(
            datetime.date(2018, 2, 18),
            categories=[
                Category(
                    'Category',
                    [
                        Meal(
                            'Meal',
                            prices=Prices(
                                other=123,
                                pupil=234,
                                student=345,
                                employee=456,
                            ),
                            notes=Notes(['Note'])
                        )
                    ]
                )
            ]
        ),
    ])
    assert canteen.to_string() == (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<openmensa xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://openmensa.org/open-mensa-v2" version="2.1" xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">\n'
        '  <canteen>\n'
        '    <day date="2018-02-18">\n'
        '      <category name="Category">\n'
        '        <meal>\n'
        '          <name>Meal</name>\n'
        '          <note>Note</note>\n'
        '          <price role="employee">4.56</price>\n'
        '          <price role="other">1.23</price>\n'
        '          <price role="pupil">2.34</price>\n'
        '          <price role="student">3.45</price>\n'
        '        </meal>\n'
        '      </category>\n'
        '    </day>\n'
        '  </canteen>\n'
        '</openmensa>\n'
    )


def test_canteen_xml():
    canteen = Canteen(days=[
        Day(
            datetime.date(2018, 2, 18),
            categories=[Category('Category', [Meal('Meal')])]
        ),
    ])
    expected_xml = ET.fromstring(
        '<openmensa version="2.1" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns="http://openmensa.org/open-mensa-v2" '
        'xsi:schemaLocation="http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd">'
        '<canteen>'
        '<day date="2018-02-18">'
        '<category name="Category">'
        '<meal><name>Meal</name></meal>'
        '</category>'
        '</day>'
        '</canteen>'
        '</openmensa>'
    )
    assert ET.tostring(canteen.to_xml()) == ET.tostring(expected_xml)


def test_day_given_empty_category_then_raises():
    with pytest.raises(ValueError):
        Day(datetime.date(2018, 2, 19), [])


def test_day_xml():
    day = Day(
        datetime.date(2018, 2, 19),
        categories=[Category('Test Category', [Meal('Test Meal')])]
    )
    expected_xml = ET.fromstring(
        '<day date="2018-02-19">'
        '<category name="Test Category">'
        '<meal>'
        '<name>Test Meal</name>'
        '</meal>'
        '</category>'
        '</day>'
    )
    assert ET.tostring(day.to_xml()) == ET.tostring(expected_xml)


def test_closed_day_xml():
    day = ClosedDay(datetime.date(2018, 2, 20))
    expected_xml = ET.fromstring(
        '<day date="2018-02-20"><closed/></day>'
    )
    assert ET.tostring(day.to_xml()) == ET.tostring(expected_xml)


def test_category_xml():
    category = Category('Test Category', [Meal('Test Meal')])
    expected_xml = ET.fromstring(
        '<category name="Test Category">'
        '<meal><name>Test Meal</name></meal>'
        '</category>'
    )
    assert ET.tostring(category.to_xml()) == ET.tostring(expected_xml)


def test_meal_sets_default_prices_and_notes():
    meal = Meal('Empty meal')
    assert meal.prices is None
    assert meal.notes == Notes()


def test_meal_xml():
    meal = Meal('Test Meal', Prices(134), Notes(['Test note']))
    expected_xml = ET.fromstring(
        '<meal>'
        '<name>Test Meal</name>'
        '<note>Test note</note>'
        '<price role="other">1.34</price>'
        '</meal>'
    )
    assert ET.tostring(meal.to_xml()) == ET.tostring(expected_xml)


def test_prices_raises_error_if_no_amount_set():
    with pytest.raises(ValueError):
        Prices()


def test_prices_sets_default_role():
    prices = Prices(123)
    assert prices.prices['other'] == 123


def test_prices_xml():
    prices = Prices(other=123, pupil=345, student=100, employee=234)

    expected_xmls = [
        ET.fromstring('<price role="employee">2.34</price>'),
        ET.fromstring('<price role="other">1.23</price>'),
        ET.fromstring('<price role="pupil">3.45</price>'),
        ET.fromstring('<price role="student">1.00</price>'),
    ]

    for price_xml, expected_xml in zip_longest(prices.to_xml(), expected_xmls):
        assert ET.tostring(price_xml) == ET.tostring(expected_xml)


def test_notes_sets_default_list():
    notes = Notes()
    assert notes.note_list == []


def test_notes_given_empty_item_then_raises():
    with pytest.raises(ValueError):
        Notes([''])


def test_notes_xml():
    notes = Notes(['Second note', 'First note'])
    expected_xmls = [
        ET.fromstring('<note>First note</note>'),
        ET.fromstring('<note>Second note</note>'),
    ]
    for note_xml, expected_xml in zip_longest(notes.to_xml(), expected_xmls):
        assert ET.tostring(note_xml) == ET.tostring(expected_xml)
