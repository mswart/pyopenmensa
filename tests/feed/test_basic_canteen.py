# -*- coding: UTF-8 -*-
import pytest
from datetime import date

from pyopenmensa.feed import BaseBuilder


@pytest.fixture
def canteen():
    return BaseBuilder()


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
