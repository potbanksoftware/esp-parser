#!/usr/bin/env python3
#
#  _csno.py
"""
CSNO record type.
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from io import BytesIO
from typing import Iterator

# this package
from esp_parser.subrecords import EDID
from esp_parser.types import CStringRecord, Record, RecordType

__all__ = ["CSNO"]


class CSNO(Record):
	"""
	Casino
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	# class DATA(RecordType):
	# 	"""
	# 	Data.
	# 	"""

	class MODL(CStringRecord):
		"""
		Casino $1 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino $5 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino $10 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino $25 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino $100 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino $500 Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Casino Roulette Chip Model.
		"""

	class MODL(CStringRecord):
		"""
		Slot Machine Model.
		"""

	class MOD2(CStringRecord):
		"""
		Slot Machine Model.

		Duplicate?
		"""

	class MOD3(CStringRecord):
		"""
		BlackJack Table Model.
		"""

	class MOD4(CStringRecord):
		"""
		Roulette Table Model.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 1.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 2.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 3.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 4.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 5.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol 6.
		"""

	class ICON(CStringRecord):
		"""
		Slot Reel Texture - Symbol W.
		"""

	class ICO2(CStringRecord):
		"""
		BlackJack Texture - Deck 1.
		"""

	class ICO2(CStringRecord):
		"""
		BlackJack Texture - Deck 2.
		"""

	class ICO2(CStringRecord):
		"""
		BlackJack Texture - Deck 3.
		"""

	class ICO2(CStringRecord):
		"""
		BlackJack Texture - Deck 4.
		"""

	@classmethod
	def parse_subrecords(cls, raw_bytes: BytesIO) -> Iterator[RecordType]:
		"""
		Parse this record's subrecords.

		:param raw_bytes: Raw bytes for this record's subrecords
		"""

		while True:
			record_type = raw_bytes.read(4)
			if not record_type:
				break

			if record_type == b"EDID":
				yield EDID.parse(raw_bytes)
			elif record_type in {b"DATA", b"FULL", b"ICO2", b"ICON", b"MOD2", b"MOD3", b"MOD4", b"MODL"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
