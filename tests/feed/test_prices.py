# -*- coding: UTF-8 -*-
import pytest
import re

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

    def test_single_cent_converting(self):
        assert convertPrice('as 3,4 € hans') == 340
        with pytest.raises(ValueError):
            convertPrice('3,4 ')

    def test_garbage_strings(self):
        with pytest.raises(ValueError):
            convertPrice('34,3,3 €')

    def test_float2price_convert(self):
        assert convertPrice(3.00) == 300
        assert convertPrice(3.65) == 365
        assert convertPrice(3.61234) == 361
        assert convertPrice(13.25534) == 1326

    def test_none_detected(self):
        assert convertPrice('-') is None
        assert convertPrice(' -   ') is None

    def test_deactived_none_detected(self):
        with pytest.raises(ValueError):
            convertPrice('-', none_regex=None)
        with pytest.raises(ValueError):
            convertPrice(' -   ', none_regex=None)

    def test_custom_none_detected(self):
        convertPrice('Keine Ahnung', none_regex=re.compile(r'[Kk]eine.*')) is None
        convertPrice('Keine Idee', none_regex=re.compile(r'[Kk]eine.*')) is None

    def test_custom_str2price_convert(self):
        class CustomStr(str): pass

        assert convertPrice(CustomStr('3.04 €')) == 304
        assert convertPrice(CustomStr('3.04€')) == 304
        assert convertPrice(CustomStr('3.04')) == 304
        assert convertPrice(CustomStr('13.04 €')) == 1304

    def test_custom_int2price_convert(self):
        class CustomInt(int): pass

        assert convertPrice(CustomInt(3)) == 3
        assert convertPrice(CustomInt(365)) == 365
        assert convertPrice(CustomInt(361)) == 361
        assert convertPrice(CustomInt(1326)) == 1326

    def test_custom_float2price_convert(self):
        class CustomFloat(float): pass

        assert convertPrice(CustomFloat(3.00)) == 300
        assert convertPrice(CustomFloat(3.65)) == 365
        assert convertPrice(CustomFloat(3.61234)) == 361
        assert convertPrice(CustomFloat(13.25534)) == 1326

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

    single_price_example = {
        'student': 364
    }

    def test_dict_passthrought(self):
        d = {
            'student': 354,
            'other': 375
        }
        assert buildPrices(d) == d

    def test_custom_dict_passthrough(self):
        class CustomDict(dict): pass

        d = CustomDict()
        d['student'] = 354
        d['other'] = 375

        assert buildPrices(d) == d

    def test_dict_type_converting(self):
        d = {'student': '3.64 €', 'employee': 3.84, 'others': 414}
        assert buildPrices(d) == self.price_example

    def test_dict_converting_with_none_clearing(self):
        d = {
            'student': '-',
            'other': 375
        }
        assert buildPrices(d) == {'other': 375}

    def test_dict_converting_with_complete_none_clearing(self):
        d = {
            'student': '-',
            'other': '  -   '
        }
        assert buildPrices(d) == {}

    def test_build_from_prices_and_roles(self):
        assert buildPrices(
            ['3.64€', 3.84, 414],
            ('student', 'employee', 'others')
        ) == self.price_example

    def test_build_from_prices_and_roles_with_custom_types(self):
        class CustomStr(str): pass
        class CustomFloat(float): pass
        class CustomInt(int): pass

        assert buildPrices(
            [CustomStr('3.64€'), CustomFloat(3.84), CustomInt(414)],
            ('student', 'employee', 'others')
        ) == self.price_example

    def test_build_from_prices_and_roles_with_none_clearing(self):
        assert buildPrices(
            ['3.64€', '-', '  -   '],
            ('student', 'employee', 'others')
        ) == self.single_price_example

    def test_build_from_prices_and_roles_with_complete_none_clearing(self):
        assert buildPrices(
            ['-', '-', '  -   '],
            ('student', 'employee', 'others')
        ) == {}

    def test_addtional_charges(self):
        assert buildPrices(
            3.64,
            default='student',
            additional={'employee': '0.20€', 'others': 50}
        ) == self.price_example

    def test_addtional_charges_with_none_clearing(self):
        assert buildPrices(
            '-',
            default='student',
            additional={'employee': '0.20€', 'others': 50}
        ) == {}

    def test_addtional_charges_with_none_clearing2(self):
        assert buildPrices(
            364,
            default='student',
            additional={'employee': '-', 'others': 50}
        ) == {'student': 364, 'others': 414}

    def test_build_from_custom_str_subtype(self):
        class CustomStr(str): pass

        assert buildPrices(
            CustomStr('3.64€'),
            default='student',
        ) == self.single_price_example

    def test_build_from_custom_int_subtype(self):
        class CustomInt(int): pass

        assert buildPrices(
            CustomInt(364),
            default='student',
        ) == self.single_price_example

    def test_build_from_custom_float_subtype(self):
        class CustomFloat(float): pass

        assert buildPrices(
            CustomFloat(3.64),
            default='student',
        ) == self.single_price_example

    def test_wrong_price_types(self):
        with pytest.raises(TypeError):
            buildPrices(True)
        with pytest.raises(TypeError):
            buildPrices(None)
