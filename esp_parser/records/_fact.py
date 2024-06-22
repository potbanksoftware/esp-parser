#!/usr/bin/env python3
#
#  _fact.py
"""
FACT record type.
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
import struct
from io import BytesIO
from typing import Iterator, Type

# 3rd party
import attrs
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, XNAM
from esp_parser.types import CStringRecord, Float32Record, Int32Record, Record, RecordType

__all__ = ["FACT"]


class FACT(Record):
	"""
	Faction.
	"""

	class FULL(CStringRecord):
		"""
		Name.
		"""

	@attrs.define
	class DATA(RecordType):
		"""
		Data.
		"""

		#: See https://tes5edit.github.io/fopdoc/Fallout3/Records/FACT.html for flags
		flags1: int
		flags2: int
		unused: bytes

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x04\x00"  # size field
			return cls(*struct.unpack("<BB2s", raw_bytes.read(4)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA\x04\x00" + struct.pack("<BB2s", self.flags1, self.flags2, self.unused)

	class CNAM(Float32Record):
		"""
		Unused.
		"""

	class RNAM(Int32Record):
		"""
		Rank Number.
		"""

	class MNAM(CStringRecord):
		"""
		Male.
		"""

	class FNAM(CStringRecord):
		"""
		Male.
		"""

	class INAM(CStringRecord):
		"""
		Insignia (unused).
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
			elif record_type == b"XNAM":
				yield XNAM.parse(raw_bytes)
			elif record_type in {
					b"FULL",
					b"DATA",
					b"CNAM",
					b"RNAM",
					b"MNAM",
					b"FNAM",
					b"INAM",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			else:
				raise NotImplementedError(record_type)
