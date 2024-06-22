#!/usr/bin/env python3
#
#  _aloc.py
"""
ALOC record type.
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
from esp_parser.types import (
		CStringRecord,
		Float32Record,
		FormIDRecord,
		RawBytesRecord,
		Record,
		RecordType,
		Uint32Record
		)

__all__ = ["ALOC"]


class ALOC(Record):
	"""
	Media Location Controller.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	class NAM1(RawBytesRecord):
		"""
		??.

		Possibly a combination of flags and enums.
		"""

	class NAM2(RawBytesRecord):
		"""
		??.
		"""

	class NAM3(RawBytesRecord):
		"""
		??.
		"""

	class NAM4(Float32Record):
		"""
		Location Delay.
		"""

	class NAM5(Uint32Record):
		"""
		Day Start.
		"""

	class NAM6(Uint32Record):
		"""
		Night Start.
		"""

	class NAM7(Float32Record):
		"""
		Retrigger Delay.
		"""

	class HNAM(FormIDRecord):
		"""
		Neutral Media Set.

		FormID of a MSET record.
		"""

	class ZNAM(FormIDRecord):
		"""
		Ally Media Set.

		FormID of a MSET record.
		"""

	class XNAM(FormIDRecord):
		"""
		Friend Media Set.

		FormID of a MSET record.
		"""

	class YNAM(FormIDRecord):
		"""
		Enemy Media Set.

		FormID of a MSET record.
		"""

	class LNAM(FormIDRecord):
		"""
		Location Media Set.

		FormID of a MSET record.
		"""

	class GNAM(FormIDRecord):
		"""
		Battle Media Set.

		FormID of a MSET record.
		"""

	class RNAM(FormIDRecord):
		"""
		Conditional Faction.

		FormID of a FACT record.
		"""

	class FNAM(RawBytesRecord):
		"""
		??.
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
					b"NAM1",
					b"NAM2",
					b"NAM3",
					b"NAM4",
					b"NAM5",
					b"NAM6",
					b"NAM7",
					b"HNAM",
					b"ZNAM",
					b"XNAM",
					b"YNAM",
					b"LNAM",
					b"GNAM",
					b"RNAM",
					b"FNAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
