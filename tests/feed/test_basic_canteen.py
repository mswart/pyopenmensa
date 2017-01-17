# -*- coding: UTF-8 -*-
import pytest
from datetime import date

from pyopenmensa.feed import BaseBuilder


@pytest.fixture
def canteen_version():
    return "1.0.3a"


@pytest.fixture
def canteen():
    return BaseBuilder()


def test_version(canteen, canteen_version):
    assert canteen.version is None
    canteen.version = canteen_version
    assert canteen.version == canteen_version
    canteen.version = None
    assert canteen.version is None


def test_day_count(canteen):
    day = date(2013, 3, 7)
    assert canteen.dayCount() == 0
    canteen._days[day] = {}
    assert canteen.dayCount() == 1
    canteen.clearDay(day)
    assert canteen.dayCount() == 0


def test_has_meals_for(canteen):
    day = date(2013, 3, 7)
    assert canteen.hasMealsFor(day) is False
    canteen._days[day] = {'Hausgericht': ('Gulash', [], {})}
    assert canteen.hasMealsFor(day) is True
    canteen.setDayClosed(day)
    assert canteen.hasMealsFor(day) is False


def test_add_meal(canteen):
    day = date(2013, 3, 7)
    canteen.addMeal(day, 'Hauptgericht', 'Gulasch')
    assert canteen.hasMealsFor(day)


def test_too_long_meal_name(canteen):
    day = date(2013, 3, 7)
    with pytest.raises(ValueError):
        canteen.addMeal(day, 'Hauptgericht', 'Y'*251)
    assert canteen.dayCount() == 0


def test_empty_meal_name(canteen):
    day = date(2013, 3, 7)
    with pytest.raises(ValueError):
        canteen.addMeal(day, 'Hauptgericht', '')
    assert canteen.dayCount() == 0


def test_empty_category_name(canteen):
    day = date(2013, 3, 7)
    with pytest.raises(ValueError):
        canteen.addMeal(day, '', 'Hunger!')
    assert canteen.dayCount() == 0


def test_empty_note(canteen):
    day = date(2013, 3, 7)
    with pytest.raises(ValueError):
        canteen.addMeal(day, 'Hauptegericht', 'Hunger!', [''])
    with pytest.raises(ValueError):
        canteen.addMeal(day, 'Hauptegericht', 'Hunger!', ['Otto', ''])
    assert canteen.dayCount() == 0


def test_known_price_roles(canteen):
    day = date(2013, 3, 7)
    prices = {
        'pupil': 12,
        'student': 12,
        'employee': 13,
        'other': 14
    }
    assert canteen.dayCount() == 0
    canteen.addMeal(day, 'Hauptgericht', 'Essen', [], prices)
    assert canteen.dayCount() == 1


def test_exception_on_unknown_price_role(canteen):
    day = date(2013, 3, 7)
    with pytest.raises(ValueError):
        canteen.addMeal(day, 'Hauptgericht', 'Essen', [], {'foobar': 12})
    assert canteen.dayCount() == 0


def test_expection_on_wrong_price_type(canteen):
    day = date(2013, 3, 7)
    wrong_types = ['12', 0.12, None]
    for value in wrong_types:
        with pytest.raises(TypeError):
            canteen.addMeal(day, 'Hauptgericht', 'Essen', [],
                            {'student': value})
    assert canteen.dayCount() == 0


def test_support_of_custom_integers_as_price_value(canteen):
    class CustomInt(int):
        pass
    day = date(2013, 3, 7)
    assert canteen.dayCount() == 0
    canteen.addMeal(day, 'Hauptgericht', 'Essen', [],
                    {'student': CustomInt(12)})
    assert canteen.dayCount() == 1
