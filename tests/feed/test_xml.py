# -*- coding: UTF-8 -*-
from datetime import date
import pytest
from xml.etree.ElementTree import fromstring as parse

from pyopenmensa.feed import BaseBuilder, LazyBuilder


PARSER_VERSION = "1.0.3a"


@pytest.fixture(params=['base', 'lazy'])
def canteen(request):
    if request.param == 'base':
        builder = BaseBuilder()
    else:
        builder = LazyBuilder()

    builder.set_version(PARSER_VERSION)
    return builder


def tag(name):
    return '{http://openmensa.org/open-mensa-v2}' + name


def find_child(parsed, tag_name, is_openmensa_tag=True):
    tag_name = tag_name if not is_openmensa_tag else tag(tag_name)
    element = parsed.find("./{}".format(tag_name))
    if element is None:
        raise KeyError("Element named {!r} not found.".format(tag_name))
    return element


def test_xml_header(canteen):
    dump = canteen.toXMLFeed()
    assert dump.startswith('<?xml version="1.0" encoding="UTF-8"?>')


def test_root_element(canteen):
    parsed = parse(canteen.toXMLFeed())
    assert parsed.tag == tag('openmensa')
    assert parsed.attrib['version'] == '2.1'
    sL = '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'
    assert parsed.attrib[sL] == 'http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd'


def test_canteen_element(canteen):
    parsed = parse(canteen.toXMLFeed())
    assert len(parsed) == 2
    canteen = find_child(parsed, 'canteen')
    version = find_child(parsed, 'version')
    assert canteen.tag == tag('canteen')
    assert len(canteen.attrib.keys()) == 0
    assert version.text == PARSER_VERSION


def test_feed_without_version(canteen):
    canteen.set_version(None)
    parsed = parse(canteen.toXMLFeed())
    get_version = lambda: find_child(parsed, 'version')
    pytest.raises(KeyError, get_version)


def test_closed_day(canteen):
    canteen.setDayClosed(date(2013, 10, 13))
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    assert len(canteen) == 1
    day = canteen[0]
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
    canteen = find_child(parsed, 'canteen')
    assert len(canteen) == 3
    for day in canteen:
        assert day.tag == tag('day')
        assert len(day.attrib) == 1
    assert canteen[0].attrib['date'] == '2013-09-13'
    assert canteen[1].attrib['date'] == '2013-10-03'
    assert canteen[2].attrib['date'] == '2013-10-13'


def test_single_category(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch')
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Nudeln')
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    assert len(canteen[0]) == 1
    category = canteen[0][0]
    assert category.tag == tag('category')
    assert len(category.attrib) == 1
    assert category.attrib['name'] == 'Hauptgerichte'
    assert len(category) == 2
    assert category[0].tag == tag('meal')
    assert category[1].tag == tag('meal')


def test_multiple_categories(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Neu', 'Gulasch')
    canteen.addMeal(date(2013, 10, 13), 'Immer', 'Nudeln')
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    day = canteen[0]
    assert len(day) == 2
    for category in day:
        assert category.tag == tag('category')
        assert len(category.attrib) == 1
    assert day[0].attrib['name'] == 'Neu'
    assert day[1].attrib['name'] == 'Immer'


def test_meal(canteen):
    canteen.addMeal(date(2013, 10, 13), 'Hauptgerichte', 'Gulasch')
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    category = canteen[0][0]
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
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    meal = canteen[0][0][0]
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
    parsed = parse(canteen.toXMLFeed())
    canteen = find_child(parsed, 'canteen')
    meal = canteen[0][0][0]
    assert len(meal) == 1 + len(prices_input)
    xml_prices = {}
    for element in meal:
        if element.tag == tag('price'):
            assert list(element.attrib.keys()) == ['role']
            xml_prices[element.attrib['role']] = element.text.strip()
    assert xml_prices == prices_output
