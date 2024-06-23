#!/usr/bin/env python3
#
#  _door.py
"""
DOOR record type.
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
from esp_parser.subrecords import EDID, OBND, Model
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType, Uint8Record

__all__ = ["DOOR"]


class DOOR(Record):
	"""
	Dialog topic.
	"""

	class FULL(CStringRecord):
		"""
		Name of the topic.
		"""

	class SCRI(FormIDRecord):
		"""
		Form ID of a :class:`~.SCPT` record.
		"""

	class SNAM(FormIDRecord):
		"""
		Sound - open.

		Form ID of a :class:`~.SOUN` record.
		"""

	class ANAM(FormIDRecord):
		"""
		Sound - close.

		Form ID of a :class:`~.SOUN` record.
		"""

	class BNAM(FormIDRecord):
		"""
		Sound - looping.

		Form ID of a :class:`~.SOUN` record.
		"""

	class FNAM(Uint8Record):
		"""
		Flags.

		See https://tes5edit.github.io/fopdoc/Fallout3/Records/DOOR.html
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
			elif record_type == b"OBND":
				yield OBND.parse(raw_bytes)
			elif record_type in {b"ANAM", b"BNAM", b"FNAM", b"FULL", b"SCRI", b"SNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
