# -*- coding: UTF-8 -*-
from datetime import date
import pytest

from pyopenmensa.feed import extractDate



class TestExtractDateFormats():

	date = date(2013, 3, 7)


	def test_passing_of_date_objects(self):
		assert extractDate(self.date) is self.date


	def test_dd_mm_yyyy(self):
		assert extractDate('07.03.2013') == self.date

	def test_d_mm_yyyy(self):
		assert extractDate('7.03.2013') == self.date

	def test_dd_m_yyyy(self):
		assert extractDate('07.3.2013') == self.date

	def test_d_m_yyyy(self):
		assert extractDate('7.3.2013') == self.date

	def test_dd_mm_yy(self):
		assert extractDate('07.03.13') == self.date

	def test_d_mm_yy(self):
		assert extractDate('7.03.13') == self.date

	def test_dd_m_yy(self):
		assert extractDate('07.3.13') == self.date

	def test_d_m_yy(self):
		assert extractDate('7.3.13') == self.date


	def test_yyyy_mm_dd(self):
		assert extractDate('2013-03-07') == self.date

	def test_yyyy_mm_d(self):
		assert extractDate('2013-03-7') == self.date

	def test_yyyy_m_dd(self):
		assert extractDate('2013-3-07') == self.date

	def test_yyyy_m_d(self):
		assert extractDate('2013-3-7') == self.date

	def test_yy_mm_dd(self):
		assert extractDate('13-03-07') == self.date

	def test_yy_mm_d(self):
		assert extractDate('13-03-7') == self.date

	def test_yy_m_dd(self):
		assert extractDate('13-3-07') == self.date

	def test_yy_m_d(self):
		assert extractDate('13-3-7') == self.date


	def test_ddDOT_ENNAME_yyyy(self):
		assert extractDate('07. March 2013') == self.date
		assert extractDate('07. march 2013') == self.date
		assert extractDate('07.March 2013') == self.date
		assert extractDate('07.march 2013') == self.date

	def test_dd_ENNAME_yyyy(self):
		assert extractDate('07 March 2013') == self.date
		assert extractDate('07 march 2013') == self.date
		assert extractDate('07March 2013') == self.date
		assert extractDate('07march 2013') == self.date

	def test_ddDOT_ENNAME_yy(self):
		assert extractDate('07. March 13') == self.date
		assert extractDate('07. march 13') == self.date
		assert extractDate('07.March 13') == self.date
		assert extractDate('07.march 13') == self.date

	def test_dd_ENNAME_yy(self):
		assert extractDate('07 March 13') == self.date
		assert extractDate('07 march 13') == self.date
		assert extractDate('07March 13') == self.date
		assert extractDate('07march 13') == self.date


	def test_ddDOT_DENAME_yyyy(self):
		assert extractDate('07. März 2013') == self.date
		assert extractDate('07. Maerz 2013') == self.date
		assert extractDate('07.März 2013') == self.date
		assert extractDate('07.Maerz 2013') == self.date

	def test_dd_DENAME_yyyy(self):
		assert extractDate('07 März 2013') == self.date
		assert extractDate('07 Maerz 2013') == self.date
		assert extractDate('07März 2013') == self.date
		assert extractDate('07Maerz 2013') == self.date

	def test_ddDOT_DENAME_yy(self):
		assert extractDate('07. März 13') == self.date
		assert extractDate('07. Maerz 13') == self.date
		assert extractDate('07.März 13') == self.date
		assert extractDate('07.Maerz 13') == self.date

	def test_dd_DENAME_yy(self):
		assert extractDate('07 März 13') == self.date
		assert extractDate('07 Maerz 13') == self.date
		assert extractDate('07März 13') == self.date
		assert extractDate('07Maerz 13') == self.date


	def test_unknown_month(self):
		with pytest.raises(ValueError):
			extractDate('07. Hans 2013')


	def test_unknown_date_format(self):
		with pytest.raises(ValueError):
			extractDate('2050.11-24')
