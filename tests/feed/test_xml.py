# -*- coding: UTF-8 -*-
from datetime import date
import pytest
from xml.etree.ElementTree import fromstring as parse

from pyopenmensa.feed import BasicCanteen, LazyCanteen


@pytest.fixture(params=['basic', 'lazy'])
def canteen(request):
    if request.param == 'basic':
        return BasicCanteen()
    else:
        return LazyCanteen()


def tag(name):
    return '{http://openmensa.org/open-mensa-v2}' + name


def test_xml_header(canteen):
    dump = canteen.toXMLFeed()
    assert dump.startswith('<?xml version="1.0" encoding="UTF-8"?>')


def test_root_element(canteen):
    parsed = parse(canteen.toXMLFeed())
    assert parsed.tag == tag('openmensa')
    assert parsed.attrib['version'] == '2.0'
    sL = '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'
    assert parsed.attrib[sL] == 'http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd'


def test_canteen_element(canteen):
    parsed = parse(canteen.toXMLFeed())
    assert len(parsed) == 1
    canteen = parsed[0]
    assert canteen.tag == tag('canteen')
    assert len(canteen.attrib.keys()) == 0


def test_closed_day(canteen):
    canteen.setDayClosed(date(2013, 10, 13))
    parsed = parse(canteen.toXMLFeed())
    assert len(parsed[0]) == 1
    day = parsed[0][0]
    assert day.tag == tag('day')
    assert len(day.attrib) == 1
    assert day.attrib['date'] == '2013-10-13'
    assert len(day) == 1
    assert day[0].tag == tag('closed')
    assert len(day[0].attrib) == 0


def test_day_sorting(canteen):
    canteen.setDayClosed(date(2013, 9, 13))
    canteen.setDayClosed(date(2013, 10, 13))
    canteen.setDayClosed(date(2013, 10, 3))
    parsed = parse(canteen.toXMLFeed())
    assert len(parsed[0]) == 3
    days = parsed[0]
    for day in days:
        assert day.tag == tag('day')
        assert len(day.attrib) == 1
    assert days[0].attrib['date'] == '2013-09-13'
    assert days[1].attrib['date'] == '2013-10-03'
    assert days[2].attrib['date'] == '2013-10-13'


def test_single_category(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch')
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Nudeln')
    parsed = parse(canteen.toXMLFeed())
    assert len(parsed[0][0]) == 1
    category = parsed[0][0][0]
    assert category.tag == tag('category')
    assert len(category.attrib) == 1
    assert category.attrib['name'] == 'Hauptgerichte'
    assert len(category) == 2
    assert category[0].tag == tag('meal')
    assert category[1].tag == tag('meal')


def test_multiple_categories(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Neu', 'Gulasch')
    canteen.addMeal(date(2013, 10, 13), 'Immer', 'Nudeln')
    day = parse(canteen.toXMLFeed())[0][0]
    assert len(day) == 2
    for category in day:
        assert category.tag == tag('category')
        assert len(category.attrib) == 1
    assert day[0].attrib['name'] == 'Neu'
    assert day[1].attrib['name'] == 'Immer'


def test_meal(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch')
    category = parse(canteen.toXMLFeed())[0][0][0]
    assert len(category) == 1
    meal = category[0]
    assert meal.tag == tag('meal')
    assert len(meal.attrib) == 0
    assert len(meal) == 1
    assert meal[0].tag == tag('name')
    assert meal[0].text.strip() == 'Gulasch'


def test_notes(canteen):
    notes = ['vegan', 'Schwein', 'glutenfrei']
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch', notes)
    meal = parse(canteen.toXMLFeed())[0][0][0][0]
    assert len(meal) == 1 + len(notes)
    xml_notes = []
    for element in meal:
        if element.tag == tag('note'):
            xml_notes.append(element.text.strip())
    assert xml_notes == notes


def test_prices(canteen):
    prices_input = {'student': 940, 'other': 9}
    prices_output = {'student': '9.40', 'other': '0.09'}
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch', prices=prices_input)
    meal = parse(canteen.toXMLFeed())[0][0][0][0]
    assert len(meal) == 1 + len(prices_input)
    xml_prices = {}
    for element in meal:
        if element.tag == tag('price'):
            assert list(element.attrib.keys()) == ['role']
            xml_prices[element.attrib['role']] = element.text.strip()
    assert xml_prices == prices_output
