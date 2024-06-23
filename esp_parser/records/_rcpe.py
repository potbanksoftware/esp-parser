#!/usr/bin/env python3
#
#  _rcpe.py
"""
RCPE record type.
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
from typing import Iterator, Tuple

# 3rd party
import attrs

# this package
from esp_parser.subrecords import CTDA, EDID
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, StructRecord, Uint32Record

__all__ = ["RCPE"]


class RCPE(Record):
	"""
	Recipe.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		skill: int
		level: int

		#: Form ID of a :class:`~.RCCT` record.
		category: bytes

		#: Form ID of a :class:`~.RCCT` record.
		sub_category: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<iI4s4s", 16

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return ("skill", "level", "category", "sub_category")

	class RCIL(FormIDRecord):
		"""
		Item.

		Form ID of an :class:`~.ARMO`, :class:`~.AMMO`, :class:`~.MISC`,
		:class:`~.WEAP`, :class:`~.BOOK`, :class:`~.KEYM`, :class:`~.ALCH`,
		:class:`~.NOTE`, :class:`~.IMOD`, :class:`~.CMNY`, :class:`~.CCRD`,
		:class:`~.CHIP` or :class:`~.LIGH` record.
		"""

	class RCQY(Uint32Record):
		"""
		Quantity.
		"""

	class RCOD(FormIDRecord):
		"""
		Unknown.
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
			elif record_type == b"CTDA":
				yield CTDA.parse(raw_bytes)
			elif record_type in {b"FULL", b"DATA", b"RCIL", b"RCQY", b"RCOD"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
