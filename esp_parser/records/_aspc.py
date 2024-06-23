#!/usr/bin/env python3
#
#  _aspc.py
"""
ASPC record type.
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
from esp_parser.subrecords import EDID, OBND
from esp_parser.types import FormIDRecord, Record, RecordType, Uint32Record

__all__ = ["ASPC"]


class ASPC(Record):
	"""
	Acoustic Space.
	"""

	class SNAM(FormIDRecord):
		"""
		Dawn / Default Loop, or Afternoon, or Dusk, or Night, or Walla.

		Form ID of a :class:`~.SOUN` record, or null.
		"""

	class WNAM(Uint32Record):
		"""
		Walla Trigger Count.
		"""

	class RDAT(FormIDRecord):
		"""
		Use Sound from Region (Interiors Only).

		Form ID of a :class:`~.REGN` record.
		"""

	class ANAM(Uint32Record):
		"""
		Environment Type.

		Enum - see below for values.
		"""

	class INAM(Uint32Record):
		"""
		Is Interior.

		Enum - see values below.
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
			elif record_type in {b"ANAM", b"INAM", b"RDAT", b"SNAM", b"WNAM"}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
