# -*- coding: UTF-8 -*-
import pytest

from pyopenmensa.feed import buildLegend, extractNotes

class TestLegendBuilding():

	def test_dict_passthrought(self):
		d = {}
		assert buildLegend(d) is d

	def test_note_extraction(self):
		text = '1) Schwein a)Farbstoff'
		legend = {'1': 'Schwein', 'a': 'Farbstoff'}
		assert buildLegend({}, text=text) == legend

class TestNoteExtraction():
	legend = {'1': 'Schwein', 'a': 'Farbstoff'}

	def test_normal_passthrought(self):
		name = 'Gulash mit Hanswurst'
		notes = []
		name2, notes2 = extractNotes(name, notes)
		assert name2 is name
		assert notes2 is notes

	def test_notes_removal(self):
		name = 'Gulash (1) with Hanswurst'
		name2, notes = extractNotes(name, [], legend={})
		assert name2 == 'Gulash with Hanswurst'
		assert notes == []

	def test_multiple_notes_removal(self):
		name = 'Gulash (1) with Hanswurst (a)'
		name2, notes = extractNotes(name, [], legend={})
		assert name2 == 'Gulash with Hanswurst'
		assert notes == []

	def test_note_extraction(self):
		name = 'Gulash (1) with Hanswurst'
		name2, notes = extractNotes(name, [], legend=self.legend)
		assert name2 == 'Gulash with Hanswurst'
		assert notes == ['Schwein']

	def test_notes_extraction(self):
		name = 'Gulash (1) with Hanswurst (a)'
		name2, notes = extractNotes(name, [], legend=self.legend)
		assert name2 == 'Gulash with Hanswurst'
		assert notes == ['Schwein', 'Farbstoff']

	def test_multiple_note_extraction(self):
		name = 'Gulash (1,a) with Hanswurst'
		name2, notes = extractNotes(name, [], legend=self.legend)
		assert name2 == 'Gulash with Hanswurst'
		assert notes == ['Schwein', 'Farbstoff']

	def test_dup_note_extraction(self):
		name = 'Gulash (1) with Hanswurst (1,a)'
		name2, notes = extractNotes(name, [], legend=self.legend)
		assert name2 == 'Gulash with Hanswurst'
		assert notes == ['Schwein', 'Farbstoff']
