#!/usr/bin/env python3
#
#  _chal.py
"""
CHAL record type.
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
from esp_parser.subrecords import EDID
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, StructRecord

__all__ = ["CHAL"]


class CHAL(Record):
	"""
	Challenge.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class ICON(CStringRecord):
		"""
		Path to icon texture, when viewed in PipBoy.
		"""

	class MICO(CStringRecord):
		"""
		Path to icon texture, when viewed in upper-left message.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		Form ID of a :class:`~.SCPT` record.
		"""

	class DESC(CStringRecord):
		"""
		Description.
		"""

	@attrs.define
	class DATA(StructRecord):
		"""
		Data.
		"""

		type: int  # Enum - see https://tes5edit.github.io/fopdoc/FalloutNV/Records/CHAL.html
		threshold: int
		flags: int  # See https://tes5edit.github.io/fopdoc/FalloutNV/Records/CHAL.html
		interval: int
		value1: bytes  # Depends on ``type``
		value2: bytes  # Depends on ``type``
		value3: bytes  # Depends on ``type``

		@staticmethod
		def get_struct_and_size() -> Tuple[str, int]:
			"""
			Returns the pack/unpack struct string and the corresponding size.
			"""
			return "<IIII2s2s4s", 24

		@staticmethod
		def get_field_names() -> Tuple[str, ...]:
			"""
			Returns a list of attributes on this class in the order they should be packed.
			"""
			return (
					"type",
					"threshold",
					"flags",
					"interval",
					"value1",
					"value2",
					"value3",
					)

	class SNAM(FormIDRecord):
		"""
		Value3.

		Depends on Data.Type
		"""

	class XNAM(FormIDRecord):
		"""
		Value4.

		Depends on Data.Type
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
			elif record_type in {
					b"FULL",
					b"ICON",
					b"MICO",
					b"SCRI",
					b"DESC",
					b"DATA",
					b"SNAM",
					b"XNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
