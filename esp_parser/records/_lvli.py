#!/usr/bin/env python3
#
#  _lvli.py
"""
LVLI record type.
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
from esp_parser.subrecords import EDID, OBND, Item, Model
from esp_parser.types import FormIDRecord, Record, RecordType, StructRecord, Uint8Record

__all__ = ["LVLI"]


class LVLI(Record):
	"""
	Leveled Item.
	"""

	class LVLD(Uint8Record):
		"""
		Chance.
		"""

	class LVLF(Uint8Record):
		"""
		Flags.

		See below for values.
		"""

	class LVLG(FormIDRecord):
		"""
		Global.

		Form ID of a :class:`~.GLOB` record.
		"""

	# Leveled List Entry. collection
	#
	# See below for details.

	@attrs.define
	class LVLO(StructRecord):
		"""
		Levelled list base data.
		"""

		level: int
		unused: bytes

		reference: bytes
		"""
		Form ID of an :class:`~.ARMO`, :class:`~.AMMO`, :class:`~.MISC`,
		:class:`~.WEAP`, :class:`~.BOOK`, :class:`~.LVLI`, :class:`~.KEYM`,
		:class:`~.ALCH`, :class:`~.NOTE`, :class:`~.IMOD`, :class:`~.CMNY`,
		:class:`~.CCRD` or :class:`~.CHIP` record.
		"""

		count: int
		unused_: bytes

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""

			return "<h2s4sh2s", 12

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""

			return ("level", "unused", "reference", "count", "unused_")

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
			elif record_type == b"OBND":
				yield OBND.parse(raw_bytes)
			elif record_type == b"COED":
				yield Item.COED.parse(raw_bytes)
			elif record_type in {b"LVLD", b"LVLF", b"LVLG", b"LVLO"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
