#!/usr/bin/env python3
#
#  _keym.py
"""
KEYM record type.
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
from typing import Iterator, NamedTuple, Type

# 3rd party
from typing_extensions import Self

# this package
from esp_parser.subrecords import EDID, OBND, Destruction, Model
from esp_parser.types import CStringRecord, FormIDRecord, Record, RecordType
from esp_parser.utils import namedtuple_qualname_repr

__all__ = ["KEYM"]


class KEYM(Record):
	"""
	Key.
	"""

	class FULL(CStringRecord):
		"""
		Name/
		"""

	class ICON(CStringRecord):
		"""
		Large Icon Filename.
		"""

	class MICO(CStringRecord):
		"""
		Small Icon FIlename.
		"""

	class SCRI(FormIDRecord):
		"""
		Script.

		FormID of a SCPT record.
		"""

	class YNAM(FormIDRecord):
		"""
		Sound - Pick Up.

		FormID of a SOUN record.
		"""

	class ZNAM(FormIDRecord):
		"""
		Sound - Drop.

		FormID of a SOUN record.
		"""

	class DATA(NamedTuple):
		value: int
		weight: int

		@classmethod
		def parse(cls: Type[Self], raw_bytes: BytesIO) -> Self:
			"""
			Parse this subrecord.

			:param raw_bytes: Raw bytes for this record
			"""

			assert raw_bytes.read(2) == b"\x08\x00"  # size field
			return cls(*struct.unpack("<if", raw_bytes.read(8)))

		def unparse(self) -> bytes:
			"""
			Turn this subrecord back into raw bytes for an ESP file.
			"""

			return b"DATA" + struct.pack("<Hif", 8, *self)

		def __repr__(self) -> str:
			return namedtuple_qualname_repr(self)

	RecordType.register(DATA)

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
			elif record_type in {
					b"FULL",
					b"ICON",
					b"MICO",
					b"SCRI",
					b"YNAM",
					b"ZNAM",
					b"DATA",
					}:
				yield getattr(cls, record_type.decode()).parse(raw_bytes)
			elif record_type in Model.members:
				yield Model.parse_member(record_type, raw_bytes)
			elif record_type in Destruction.members:
				yield Destruction.parse_member(record_type, raw_bytes)
			else:
				raise NotImplementedError(record_type)
