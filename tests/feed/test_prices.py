# -*- coding: UTF-8 -*-
import pytest

from pyopenmensa.feed import convertPrice, buildPrices


class TestPriceConverting():

    def test_int2price_convert(self):
        assert convertPrice(304) == 304
        assert convertPrice(20) == 20

    def test_str_dot2price_convert(self):
        assert convertPrice('3.04 €') == 304
        assert convertPrice('3.04€') == 304
        assert convertPrice('3.04') == 304
        assert convertPrice('13.04 €') == 1304

    def test_str_comma2price_convert(self):
        assert convertPrice('3,04 €') == 304
        assert convertPrice('3,04€') == 304
        assert convertPrice('3,04') == 304
        assert convertPrice('13,04 €') == 1304

    def test_str2price_with_garbage(self):
        assert convertPrice('as 3,04 hans') == 304
        assert convertPrice('14,3 2 12,4,4 13.04') == 1304

    def test_str_only_euro(self):
        assert convertPrice('3 €') == 300
        assert convertPrice('4€') == 400

    def test_garbage_strings(self):
        with pytest.raises(ValueError):
            convertPrice('34,3,3 €')

    def test_float2price_convert(self):
        assert convertPrice(3.00) == 300
        assert convertPrice(3.65) == 365
        assert convertPrice(3.61234) == 361
        assert convertPrice(13.25534) == 1326

    def test_wrong_types(self):
        with pytest.raises(TypeError):
            convertPrice(True)
        with pytest.raises(TypeError):
            convertPrice(None)


class TestPriceDictBuilding():
    price_example = {
        'student': 364,
        'employee': 384,
        'others': 414
    }

    def test_dict_passthrought(self):
        d = {
            'student': 354,
            'other': 375
        }
        assert buildPrices(d) == d

    def test_dict_type_converting(self):
        d = {'student': '3.64 €', 'employee': 3.84, 'others': 414}
        assert buildPrices(d) == self.price_example

    def test_build_from_prices_and_roles(self):
        assert buildPrices(
            ['3.64€', 3.84, 414],
            ('student', 'employee', 'others')
        ) == self.price_example

    def test_addtional_charges(self):
        assert buildPrices(
            3.64,
            default='student',
            additional={'employee': '0.20€', 'others': 50}
        ) == self.price_example

    def test_wrong_price_types(self):
        with pytest.raises(TypeError):
            buildPrices(True)
        with pytest.raises(TypeError):
            buildPrices(None)
